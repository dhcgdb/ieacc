#include "ns3/ptr.h"
#include "ns3/log.h"
#include "ns3/simulator.h"
#include "ns3/packet.h"
#include "ns3/callback.h"
#include "ns3/string.h"
#include "ns3/uinteger.h"
#include "ns3/double.h"
#include "consumerCCs.h"
#include <limits>
#include <iostream>
#include <iomanip>
#include <random>
#include <memory>

NS_LOG_COMPONENT_DEFINE("ndn.ConsumerCCs");

namespace ns3 {
    namespace ndn {
        void cwndChangeWDCallback(ConsumerCCs* ptr)
        {
            static int x = 0;
            ptr->collectInfo.avgDelay = ptr->m_rtt->GetCurrentEstimate().GetSeconds();
            ptr->collectInfo.InflightNum = ptr->m_inFlight;

            if (ptr->log_mask & 0b1000)
                ptr->printCollectInfo(x);

            if (ptr->m_ccAlgorithm == CCType::RL) {
                ptr->transclass->SendParam2RLModule(&ptr->collectInfo);
                ptr->transclass->GetActFromRLModule(&ptr->action);
                ptr->m_window = ptr->m_window * ptr->action.new_cWnd;
                if (ptr->m_window < 1.0)
                    ptr->m_window = 1.0;
                else if (ptr->m_window > 700)
                    ptr->m_window = 700;
                if (ptr->log_mask & 0b1000)
                    std::cout << std::setiosflags(std::ios::left) << "No." << std::setw(8) << x << " new_cwnd:" << ptr->m_window << std::endl;
            }

            memset(&ptr->collectInfo, 0, sizeof(ptr->collectInfo));
            ptr->cwndChangeWD.Ping(Seconds(ptr->watchdogt));
            x++;
        }

        TransParam2Py::TransParam2Py(uint16_t id)
            : Ns3AIRL<DDPGParam, DDPGAct>(id)
        {
            SetCond(2, 0);
        }

        void TransParam2Py::SendParam2RLModule(DDPGParam* collectInfo)
        {
            auto shm_send = EnvSetterCond();
            memcpy(shm_send, collectInfo, sizeof(DDPGParam));
            SetCompleted();
        }

        void TransParam2Py::GetActFromRLModule(DDPGAct* action)
        {
            auto shm_recv = ActionGetterCond();
            memcpy(action, shm_recv, sizeof(DDPGAct));
            GetCompleted();
        }

        void ConsumerCCs::localLastDelayRecordCb(Ptr<App> optr, uint32_t seqno, Time delay, int32_t hopcount)
        {
            Ptr<ConsumerCCs> ptr = DynamicCast<ConsumerCCs>(optr);
            ptr->localLastDelay = delay.GetSeconds();
        }

        void ConsumerCCs::localFullDelayRecordCb(Ptr<App> optr, uint32_t seqno, Time delay, uint32_t retxcount, int32_t hopcount)
        {
            Ptr<ConsumerCCs> ptr = DynamicCast<ConsumerCCs>(optr);
            ptr->localFullDelay = delay.GetSeconds();
        }

        NS_OBJECT_ENSURE_REGISTERED(ConsumerCCs);

        ConsumerCCs::ConsumerCCs()
            : m_ssthresh(std::numeric_limits<double>::max())
            , m_highData(0), m_recPoint(0.0)
            , adjust(true)
        {
            memset(&collectInfo, 0, sizeof(collectInfo));
            m_firstInterestDataDelay.ConnectWithoutContext(MakeCallback(ConsumerCCs::localFullDelayRecordCb));
            m_lastRetransmittedInterestDataDelay.ConnectWithoutContext(MakeCallback(ConsumerCCs::localLastDelayRecordCb));
        }

        TypeId ConsumerCCs::GetTypeId()
        {
            static TypeId tid =
                TypeId("ns3::ndn::ConsumerCCs")
                .SetGroupName("Ndn")
                .SetParent<ConsumerWindow>()
                .AddConstructor<ConsumerCCs>()
                .AddAttribute("CcAlgorithm", "Specify which window adaptation algorithm to use",
                              EnumValue(CCType::AIMD),
                              MakeEnumAccessor(&ConsumerCCs::m_ccAlgorithm),
                              MakeEnumChecker(CCType::AIMD, "AIMD", CCType::RL, "RL",
                                              CCType::ECP, "ECP", CCType::none, "none"))

                .AddAttribute("Beta", "TCP Multiplicative Decrease factor",
                              DoubleValue(0.5),
                              MakeDoubleAccessor(&ConsumerCCs::m_beta),
                              MakeDoubleChecker<double>())

                .AddAttribute("Frequency", "",
                              DoubleValue(100.0),
                              MakeDoubleAccessor(&ConsumerCCs::SetFrequency),
                              MakeDoubleChecker<double>())

                .AddAttribute("Randomize", "",
                              StringValue("uniform"),
                              MakeStringAccessor(&ConsumerCCs::SetRandomize),
                              MakeStringChecker())

                .AddAttribute("WatchDog", "",
                              DoubleValue(0),
                              MakeDoubleAccessor(&ConsumerCCs::SetWatchDog),
                              MakeDoubleChecker<double>())

                .AddAttribute("RandomPrefix", "",
                              IntegerValue(0),
                              MakeIntegerAccessor(&ConsumerCCs::random_prefix),
                              MakeIntegerChecker<int>())

                .AddAttribute("LogMask", "bit0:data, bit1:timeout, bit2:nack",
                              IntegerValue(0),
                              MakeIntegerAccessor(&ConsumerCCs::log_mask),
                              MakeIntegerChecker<uint8_t>())

                .AddAttribute("ShmID", "",
                              IntegerValue(1024),
                              MakeIntegerAccessor(&ConsumerCCs::SetTrans),
                              MakeIntegerChecker<uint16_t>());
            return tid;
        }

        void ConsumerCCs::OnData(shared_ptr<const Data> data)
        {
            Consumer::OnData(data);
            if (m_inFlight > static_cast<uint32_t>(0)) {
                m_inFlight--;
            }
            uint64_t sequenceNum = data->getName().get(-1).toSequenceNumber();
            uint64_t congesLevel = data->getCongestionMark();
            uint64_t dataSize = data->getContent().size();

            collectInfo.cWndSum += m_window;
            collectInfo.DataNum++;
            collectInfo.congesLevelSum += congesLevel;
            collectInfo.dataSizeSum += dataSize;

            if (m_highData < sequenceNum) {
                m_highData = sequenceNum;
            }
            WindowIncrease();
            if (log_mask & 0b1) {
                std::cout << std::setiosflags(std::ios::left) << std::setprecision(12)
                    << "time," << std::setw(15) << Simulator::Now().GetSeconds()
                    << ",data,\t"
                    << ",name, " << m_interestName
                    << ",Window, " << std::setw(15) << m_window
                    << ",inFlight," << std::setw(15) << m_inFlight
                    << ",seq," << std::setw(15) << sequenceNum
                    << ",congesLevel," << std::setw(15) << congesLevel
                    << ",delay_with_retx(if have)," << std::setw(15) << localFullDelay
                    << ",delay_just_this," << std::setw(15) << localLastDelay
                    << ",rto," << std::setw(15) << m_rtt->RetransmitTimeout().GetSeconds()
                    << std::endl;
            }
            ScheduleNextPacket();
        }

        void ConsumerCCs::OnTimeout(uint32_t sequenceNum)
        {
            if (m_inFlight > static_cast<uint32_t>(0)) {
                m_inFlight--;
            }
            collectInfo.TimeoutNum++;

            if (nackDeSeq.find(sequenceNum) == nackDeSeq.end())
                WindowDecrease(false);
            nackDeSeq.erase(sequenceNum);

            Consumer::OnTimeout(sequenceNum);
            if (log_mask & 0b10) {
                std::cout << std::setiosflags(std::ios::left) << std::setprecision(12)
                    << "time," << std::setw(15) << Simulator::Now().GetSeconds()
                    << ",timeout,\t"
                    << ",name, " << m_interestName
                    << ",Window, " << std::setw(15) << m_window
                    << ",inFlight," << std::setw(15) << m_inFlight
                    << ",seq," << std::setw(15) << sequenceNum
                    << ",rto," << std::setw(15) << m_rtt->RetransmitTimeout().GetSeconds()
                    << std::endl;
            }
        }

        void ConsumerCCs::OnNack(shared_ptr<const lp::Nack> nack)
        {
            Consumer::OnNack(nack);
            lp::NackReason reason = nack->getReason();
            collectInfo.NackNum++;
            uint32_t sequenceNum = nack->getInterest().getName().get(-1).toSequenceNumber();
            if (log_mask & 0b100) {
                std::cout << std::setiosflags(std::ios::left) << std::setprecision(12)
                    << "time," << std::setw(15) << Simulator::Now().GetSeconds()
                    << ",nack,\t"
                    << ",name, " << m_interestName
                    << ",Window, " << std::setw(15) << m_window
                    << ",seq," << std::setw(15) << sequenceNum
                    << " reason:" << std::setw(15) << nack->getReason()
                    << std::endl;
            }
            if (m_ccAlgorithm == CCType::ECP) {
                if (reason == lp::NackReason::FREE)
                    adjust = true;
                else if (reason == lp::NackReason::BUSY)
                    adjust = false;
                else if (reason == lp::NackReason::CONGESTION) {
                    if (m_inFlight > static_cast<uint32_t>(0)) {
                        m_inFlight--;
                    }
                    m_rtt->SentSeq(SequenceNumber32(sequenceNum), 1);
                    m_seqTimeouts.erase(sequenceNum);
                    m_retxSeqs.insert(sequenceNum);
                    //nackDeSeq.insert(sequenceNum);  //To prevent wrong timeout decrase, comment this line if retx to save memory
                    WindowDecrease(true);
                }
            }
            if (m_ccAlgorithm == CCType::AIMD) {
                if (reason == lp::NackReason::CONGESTION) {
                    //if (m_inFlight > static_cast<uint32_t>(0)) {
                    //    m_inFlight--;
                    //}
                    //m_rtt->SentSeq(SequenceNumber32(sequenceNum), 1);
                    //m_seqTimeouts.erase(sequenceNum);
                    //m_retxSeqs.insert(sequenceNum);
                    nackDeSeq.insert(sequenceNum);  //To prevent wrong timeout decrase, comment this line if retx to save memory
                    WindowDecrease(true);
                }
            }
            ScheduleNextPacket();
        }

        void ConsumerCCs::ScheduleNextPacket()
        {
            if (random_prefix != 0) {
                static std::random_device rdev;
                static std::mt19937 reng(rdev());
                static std::uniform_int_distribution<> u(0, random_prefix);
                static std::string basename = m_interestName.toUri();
                this->SetAttribute("Prefix", StringValue(basename + "/" + std::to_string(u(reng))));
            }

            if (m_window == static_cast<uint32_t>(0)) {
                Simulator::Remove(m_sendEvent);
                m_sendEvent = Simulator::Schedule(
                    Seconds(std::min<double>(0.5, m_rtt->RetransmitTimeout().ToDouble(Time::S))),
                    &ConsumerCCs::SendPacket, this);
            }
            else if (m_inFlight >= static_cast<uint32_t>(m_window)) {
            }
            else {
                if (m_sendEvent.IsRunning()) {
                    Simulator::Remove(m_sendEvent);
                }
                if (frequency != 0 && randomSend)
                    m_sendEvent = Simulator::Schedule(Seconds(randomSend->GetValue()), &ConsumerCCs::SendPacket, this);
                else if (frequency != 0)
                    m_sendEvent = Simulator::Schedule(Seconds(1 / frequency), &ConsumerCCs::SendPacket, this);
                else
                    m_sendEvent = Simulator::ScheduleNow(&ConsumerCCs::SendPacket, this);
            }
        }

        void ConsumerCCs::printCollectInfo(int no)
        {
            std::cout << "No." << no
                << " Window:" << collectInfo.cWndSum
                << " Rtt:" << collectInfo.avgDelay
                << " Inflight:" << collectInfo.InflightNum
                << " Data:" << collectInfo.DataNum
                << " Timeout:" << collectInfo.TimeoutNum
                << " Nack:" << collectInfo.NackNum
                << " CongesLevelSum:" << collectInfo.congesLevelSum / collectInfo.DataNum
                << " DataSizeSum:" << collectInfo.dataSizeSum
                << std::endl;
        }

        void ConsumerCCs::WindowIncrease()
        {
            switch (m_ccAlgorithm) {
                case CCType::AIMD:
                    if (m_window < m_ssthresh) {
                        m_window += 1.0;
                    }
                    else {
                        m_window += (1.0 / m_window);
                    }
                    break;
                case CCType::ECP:
                    if (adjust == true)
                        m_window = m_window + 0.5;
                    else
                        m_window = m_window + 1 / m_window;
                    break;
                case CCType::RL:
                default:
                    break;
            }
        }

        void ConsumerCCs::WindowDecrease(bool nacktrig)
        {
            if (m_highData > m_recPoint) {
                const double diff = m_seq - m_highData;
                BOOST_ASSERT(diff > 0);
                m_recPoint = m_seq;
                switch (m_ccAlgorithm) {
                    case CCType::AIMD:
                        if (nacktrig) {
                            m_ssthresh = m_window * 0.5;
                            m_window = m_ssthresh;
                        }
                        else {
                            m_ssthresh = m_window * m_beta;
                            m_window = m_ssthresh;
                        }
                        break;
                    case CCType::ECP:
                        if (nacktrig)
                            m_window = m_window * 0.875;
                        else
                            m_window = m_window * 0.5;
                        break;
                    case CCType::RL:
                    default:
                        break;
                }
                if (m_setInitialWindowOnTimeout && m_window < m_initialWindow) {
                    m_window = m_initialWindow;
                }
                else if (m_window < 1)
                    m_window = 1;
            }
            else {
                NS_LOG_DEBUG("Window decrease suppressed, next change: "
                             << m_recPoint);
            }
        }

        void ConsumerCCs::SetRandomize(const std::string& value)
        {
            if (value == "uniform") {
                randomSend = CreateObject<UniformRandomVariable>();
                randomSend->SetAttribute("Min", DoubleValue(0.0));
                randomSend->SetAttribute("Max", DoubleValue(2 * 1.0 / frequency));
            }
            else if (value == "exponential") {
                randomSend = CreateObject<ExponentialRandomVariable>();
                randomSend->SetAttribute("Mean", DoubleValue(1.0 / frequency));
                randomSend->SetAttribute("Bound", DoubleValue(50.0 / frequency));
            }
            else
                randomSend = 0;
        }

        void ConsumerCCs::SetFrequency(double f)
        {
            frequency = f;
        }

        void ConsumerCCs::SetWatchDog(double t)
        {
            watchdogt = t;
            if (t > 0) {
                cwndChangeWD.Ping(Seconds(t));
                cwndChangeWD.SetFunction(cwndChangeWDCallback);
                cwndChangeWD.SetArguments<ConsumerCCs*>(this);
            }
        }

        void ConsumerCCs::SetTrans(uint16_t id)
        {
            transclass = std::make_unique<TransParam2Py>(id);
        }

        void ConsumerCCs::WillSendOutInterest(uint32_t sequenceNumber)
        {
            static int interestNum = 0;
            interestNum++;
            ConsumerWindow::WillSendOutInterest(sequenceNumber);
        }

    }
}
