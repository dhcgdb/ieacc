#include "ns3/ptr.h"
#include "ns3/log.h"
#include "ns3/simulator.h"
#include "ns3/packet.h"
#include "ns3/callback.h"
#include "ns3/string.h"
#include "ns3/uinteger.h"
#include "ns3/double.h"
#include "consumerNE.h"
#include <limits>
#include <iostream>
#include <iomanip>
#include <random>
#include <memory>
#define LOG_DATA 0b1
#define LOG_TIMEOUT 0b10
#define LOG_NACK 0b100
#define LOG_LEARNING 0b1000
#define LOG_REQ 0b10000
#define LOG_TOFILE 0b10000000

NS_LOG_COMPONENT_DEFINE("ndn.ConsumerNE");

extern double globalbw;

namespace ns3 {
    namespace ndn {
        void cwndChangeWDCallback(ConsumerNE* ptr)
        {
            static int x = 0;
            if (ptr->m_active)
                ptr->collectInfo.avgDelay = 1;
            else
                ptr->collectInfo.avgDelay = -1;
            ptr->collectInfo.cWndSum = globalbw;
            //ptr->collectInfo.cWndSum /= (ptr->collectInfo.DataNum + 1);
            //ptr->collectInfo.DataNum = ptr->collectInfo.dataSizeSum / 1024;
            //ptr->collectInfo.InflightNum = ptr->m_inFlight;

            if (ptr->log_mask & LOG_LEARNING)
                ptr->printCollectInfo(x, ptr->log_mask & LOG_TOFILE);

            if (ptr->m_ccAlgorithm == CCType::RL) {
                ptr->transclass->SendParam2RLModule(&ptr->collectInfo);
                ptr->transclass->GetActFromRLModule(&ptr->action);
                if (ptr->m_active) {
                    if (ptr->action.new_cWnd > ptr->m_window) {
                        ptr->m_window = 2 * ptr->m_window;
                        if (ptr->m_window > ptr->action.new_cWnd)
                            ptr->m_window = ptr->action.new_cWnd;
                    }
                    else
                        ptr->m_window = ptr->action.new_cWnd;
                }
                if (ptr->log_mask & LOG_LEARNING)
                    if (ptr->log_mask & LOG_TOFILE)
                        ptr->logstream << std::setiosflags(std::ios::left) << "No." << std::setw(8) << x << " new_cwnd:" << ptr->m_window << std::endl;
                    else
                        std::cout << std::setiosflags(std::ios::left) << "No." << std::setw(8) << x << " new_cwnd:" << ptr->m_window << std::endl;
            }
            memset(&ptr->collectInfo, 0, sizeof(ptr->collectInfo));
            ptr->cwndChangeWD.Ping(Seconds(ptr->watchdogt));
            x++;
        }

        TransParam2Py1::TransParam2Py1(uint16_t id)
            : Ns3AIRL<DDPGParam, DDPGAct>(id)
        {
            SetCond(2, 0);
        }

        void TransParam2Py1::SendParam2RLModule(DDPGParam* collectInfo)
        {
            auto shm_send = EnvSetterCond();
            memcpy(shm_send, collectInfo, sizeof(DDPGParam));
            SetCompleted();
        }

        void TransParam2Py1::GetActFromRLModule(DDPGAct* action)
        {
            auto shm_recv = ActionGetterCond();
            memcpy(action, shm_recv, sizeof(DDPGAct));
            GetCompleted();
        }

        void ConsumerNE::localLastDelayRecordCb(Ptr<App> optr, uint32_t seqno, Time delay, int32_t hopcount)
        {
            Ptr<ConsumerNE> ptr = DynamicCast<ConsumerNE>(optr);
            ptr->localLastDelay = delay.GetSeconds();
        }

        void ConsumerNE::localFullDelayRecordCb(Ptr<App> optr, uint32_t seqno, Time delay, uint32_t retxcount, int32_t hopcount)
        {
            Ptr<ConsumerNE> ptr = DynamicCast<ConsumerNE>(optr);
            ptr->localFullDelay = delay.GetSeconds();
        }

        NS_OBJECT_ENSURE_REGISTERED(ConsumerNE);

        ConsumerNE::ConsumerNE()
            : m_ssthresh(400)//std::numeric_limits<double>::max())
            , m_highData(0), m_recPoint(0.0)
            , adjust(true)
        {
            memset(&collectInfo, 0, sizeof(collectInfo));
            m_firstInterestDataDelay.ConnectWithoutContext(MakeCallback(ConsumerNE::localFullDelayRecordCb));
            m_lastRetransmittedInterestDataDelay.ConnectWithoutContext(MakeCallback(ConsumerNE::localLastDelayRecordCb));
        }

        TypeId ConsumerNE::GetTypeId()
        {
            static TypeId tid =
                TypeId("ns3::ndn::ConsumerNE")
                .SetGroupName("Ndn")
                .SetParent<ConsumerWindow>()
                .AddConstructor<ConsumerNE>()
                .AddAttribute("CcAlgorithm", "Specify which window adaptation algorithm to use",
                              EnumValue(CCType::AIMD),
                              MakeEnumAccessor(&ConsumerNE::m_ccAlgorithm),
                              MakeEnumChecker(CCType::AIMD, "AIMD", CCType::RL, "RL",
                                              CCType::ECP, "ECP", CCType::none, "none"))

                .AddAttribute("Beta", "TCP Multiplicative Decrease factor",
                              DoubleValue(0.5),
                              MakeDoubleAccessor(&ConsumerNE::m_beta),
                              MakeDoubleChecker<double>())

                .AddAttribute("Frequency", "",
                              DoubleValue(100.0),
                              MakeDoubleAccessor(&ConsumerNE::SetFrequency),
                              MakeDoubleChecker<double>())

                .AddAttribute("Randomize", "",
                              StringValue("uniform"),
                              MakeStringAccessor(&ConsumerNE::SetRandomize),
                              MakeStringChecker())

                .AddAttribute("WatchDog", "",
                              DoubleValue(0),
                              MakeDoubleAccessor(&ConsumerNE::SetWatchDog),
                              MakeDoubleChecker<double>())

                .AddAttribute("RandomPrefix", "",
                              StringValue(""),
                              MakeStringAccessor(&ConsumerNE::SetRandomPrefix),
                              MakeStringChecker())

                .AddAttribute("LogMask", "bit0:data, bit1:timeout, bit2:nack",
                              IntegerValue(0),
                              MakeIntegerAccessor(&ConsumerNE::log_mask),
                              MakeIntegerChecker<uint8_t>())

                .AddAttribute("Log2File", "",
                              StringValue(""),
                              MakeStringAccessor(&ConsumerNE::SetLog2File),
                              MakeStringChecker())

                .AddAttribute("ShmID", "",
                              IntegerValue(1024),
                              MakeIntegerAccessor(&ConsumerNE::SetTrans),
                              MakeIntegerChecker<uint16_t>());
            return tid;
        }

        void ConsumerNE::OnData(shared_ptr<const Data> data)
        {
            Consumer::OnData(data);
            if (m_inFlight > static_cast<uint32_t>(0)) {
                m_inFlight--;
            }
            uint64_t sequenceNum = data->getName().get(-1).toSequenceNumber();
            uint64_t congesLevel = data->getCongestionMark();
            uint64_t dataSize = data->getContent().size();
            std::string dataname = data->getName().getPrefix(2).toUri();

            if (dataname == "/ustc/2") {
                collectInfo.cWndSum += m_window;
                collectInfo.DataNum++;
                collectInfo.congesLevelSum += congesLevel;
                //collectInfo.dataSizeSum += dataSize;
                collectInfo.avgDelay += localLastDelay;
            }
            else {
                collectInfo.cWndSum += m_window;
                collectInfo.DataNum++;
                collectInfo.congesLevelSum += congesLevel;
                collectInfo.dataSizeSum += dataSize;
                collectInfo.avgDelay += localLastDelay;
            }

            if (m_highData < sequenceNum) {
                m_highData = sequenceNum;
            }
            //if (dataname != "/ustc/2")
            WindowIncrease(dataname);
            if (log_mask & LOG_DATA) {
                if (log_mask & LOG_TOFILE)
                    logstream << std::setiosflags(std::ios::left) << std::setprecision(12)
                    << "time," << std::setw(15) << Simulator::Now().GetSeconds()
                    << ",data,\t"
                    << ",name, " << dataname
                    << ",Window, " << std::setw(15) << m_window
                    << ",inFlight," << std::setw(15) << m_inFlight
                    << ",seq," << std::setw(15) << sequenceNum
                    << ",congesLevel," << std::setw(15) << congesLevel
                    << ",delay_with_retx(if have)," << std::setw(15) << localFullDelay
                    << ",delay_just_this," << std::setw(15) << localLastDelay
                    << ",rto," << std::setw(15) << m_rtt->RetransmitTimeout().GetSeconds()
                    << std::endl;

                else
                    std::cout << std::setiosflags(std::ios::left) << std::setprecision(12)
                    << "time," << std::setw(15) << Simulator::Now().GetSeconds()
                    << ",data,\t"
                    << ",name, " << dataname
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

        void ConsumerNE::OnTimeout(uint32_t sequenceNum)
        {
            if (m_inFlight > static_cast<uint32_t>(0)) {
                m_inFlight--;
            }
            collectInfo.TimeoutNum++;

            if (nackDeSeq.find(sequenceNum) == nackDeSeq.end())
                //if (ustc2seq.find(sequenceNum) == ustc2seq.end())
                WindowDecrease(false);
            nackDeSeq.erase(sequenceNum);

            Consumer::OnTimeout(sequenceNum);
            if (log_mask & LOG_TIMEOUT) {
                if (log_mask & LOG_TOFILE)
                    logstream << std::setiosflags(std::ios::left) << std::setprecision(12)
                    << "time," << std::setw(15) << Simulator::Now().GetSeconds()
                    << ",timeout,\t"
                    << ",name, " << m_interestName
                    << ",Window, " << std::setw(15) << m_window
                    << ",inFlight," << std::setw(15) << m_inFlight
                    << ",seq," << std::setw(15) << sequenceNum
                    << ",rto," << std::setw(15) << m_rtt->RetransmitTimeout().GetSeconds()
                    << std::endl;

                else
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

        void ConsumerNE::OnNack(shared_ptr<const lp::Nack> nack)
        {
            Consumer::OnNack(nack);
            std::string nackname = nack->getInterest().getName().getPrefix(2).toUri();
            lp::NackReason reason = nack->getReason();
            collectInfo.NackNum++;
            uint32_t sequenceNum = nack->getInterest().getName().get(-1).toSequenceNumber();
            if (log_mask & LOG_NACK) {
                if (log_mask & LOG_TOFILE)
                    logstream << std::setiosflags(std::ios::left) << std::setprecision(12)
                    << "time," << std::setw(15) << Simulator::Now().GetSeconds()
                    << ",nack,\t"
                    << ",name, " << nackname
                    << ",Window, " << std::setw(15) << m_window
                    << ",seq," << std::setw(15) << sequenceNum
                    << " reason:" << std::setw(15) << nack->getReason()
                    << std::endl;

                else
                    std::cout << std::setiosflags(std::ios::left) << std::setprecision(12)
                    << "time," << std::setw(15) << Simulator::Now().GetSeconds()
                    << ",nack,\t"
                    << ",name, " << nackname
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
                    //m_rtt->SentSeq(SequenceNumber32(sequenceNum), 1);
                    //m_seqTimeouts.erase(sequenceNum);
                    //m_retxSeqs.insert(sequenceNum);
                    nackDeSeq.insert(sequenceNum);  //To prevent wrong timeout decrase, comment this line if retx to save memory
                    WindowDecrease(true);
                }
            }
            if (m_ccAlgorithm == CCType::AIMD) {
                if (reason == lp::NackReason::CONGESTION) {
                    //if (m_inFlight > static_cast<uint32_t>(0)) {
                    //    m_inFlight--;
                    //}
                    m_rtt->SentSeq(SequenceNumber32(sequenceNum), 1);
                    m_seqTimeouts.erase(sequenceNum);
                    m_retxSeqs.insert(sequenceNum);
                    //nackDeSeq.insert(sequenceNum);  //To prevent wrong timeout decrase, comment this line if retx to save memory
                    WindowDecrease(true);
                }
            }
            ScheduleNextPacket();
        }

        void ConsumerNE::ScheduleNextPacket()
        {
            if (randprefix) {
                static std::random_device rdev;
                static std::mt19937 reng(rdev());
                static std::uniform_real_distribution<> u(0, intervalp.back());
                double rnum = u(reng);
                int i;
                for (i = 0;i < intervalp.size();i++)
                    if (rnum <= intervalp[i])
                        break;
                this->SetAttribute("Prefix", StringValue(intervalmap.find(intervalp[i])->second));
            }

            if (m_window == static_cast<uint32_t>(0)) {
                Simulator::Remove(m_sendEvent);
                m_sendEvent = Simulator::Schedule(
                    Seconds(std::min<double>(0.5, m_rtt->RetransmitTimeout().ToDouble(Time::S))),
                    &ConsumerNE::SendPacket, this);
            }
            else if (m_inFlight >= static_cast<uint32_t>(m_window)) {
            }
            else {
                if (m_sendEvent.IsRunning()) {
                    Simulator::Remove(m_sendEvent);
                }
                if (frequency != 0 && randomSend)
                    m_sendEvent = Simulator::Schedule(Seconds(randomSend->GetValue()), &ConsumerNE::SendPacket, this);
                else if (frequency != 0)
                    m_sendEvent = Simulator::Schedule(Seconds(1 / frequency), &ConsumerNE::SendPacket, this);
                else
                    m_sendEvent = Simulator::ScheduleNow(&ConsumerNE::SendPacket, this);
            }
        }

        void ConsumerNE::printCollectInfo(int no, bool tofile)
        {
            if (tofile)
                logstream << "No." << no
                << " Window:" << collectInfo.cWndSum
                << " Rtt:" << collectInfo.avgDelay
                << " Inflight:" << collectInfo.InflightNum
                << " Data:" << collectInfo.DataNum
                << " Timeout:" << collectInfo.TimeoutNum
                << " Nack:" << collectInfo.NackNum
                << " CongesLevelSum:" << collectInfo.congesLevelSum / (collectInfo.DataNum + 1)
                << " DataSizeSum:" << collectInfo.dataSizeSum
                << std::endl;
            else
                std::cout << "No." << no
                << " Window:" << collectInfo.cWndSum
                << " Rtt:" << collectInfo.avgDelay
                << " Inflight:" << collectInfo.InflightNum
                << " Data:" << collectInfo.DataNum
                << " Timeout:" << collectInfo.TimeoutNum
                << " Nack:" << collectInfo.NackNum
                << " CongesLevelSum:" << collectInfo.congesLevelSum / (collectInfo.DataNum + 1)
                << " DataSizeSum:" << collectInfo.dataSizeSum
                << std::endl;
        }

        void ConsumerNE::WindowIncrease(std::string dataname)
        {
            switch (m_ccAlgorithm) {
                case CCType::AIMD:
                    if (m_window < m_ssthresh) {
                        if (dataname == "/ustc/2")
                            m_window += 1.2;
                        else
                            m_window += 1.0;
                    }
                    else {
                        if (dataname == "/ustc/2")
                            m_window += (1.25 / m_window);
                        else
                            m_window += (1.0 / m_window);
                    }
                    break;
                case CCType::ECP:
                    if (adjust == true)
                        if (dataname == "/ustc/2")
                            m_window += 0.75;
                        else
                            m_window += 0.5;
                    else
                        if (dataname == "/ustc/2")
                            m_window += (1.25 / m_window);
                        else
                            m_window += (1.0 / m_window);
                    break;
                case CCType::RL:
                default:
                    break;
            }
        }

        void ConsumerNE::WindowDecrease(bool nacktrig)
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

        void ConsumerNE::SetRandomize(const std::string& value)
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

        void ConsumerNE::SetLog2File(std::string path)
        {
            if (!path.empty()) {
                log_mask |= 1 << 7;
                logstream.open(path, std::ios::out);
                if (!logstream.is_open()) {
                    std::cout << "Can't open file \"" << path << "\"" << std::endl;
                    exit(0);
                }
            }
        }

        void ConsumerNE::SetFrequency(double f)
        {
            frequency = f;
        }

        void ConsumerNE::SetWatchDog(double t)
        {
            watchdogt = t;
            if (t > 0) {
                cwndChangeWD.Ping(Seconds(t));
                cwndChangeWD.SetFunction(cwndChangeWDCallback);
                cwndChangeWD.SetArguments<ConsumerNE*>(this);
            }
        }

        void ConsumerNE::SetTrans(uint16_t id)
        {
            transclass = std::make_unique<TransParam2Py1>(id);
        }

        void ConsumerNE::WillSendOutInterest(uint32_t sequenceNumber)
        {
            if (m_interestName == "/ustc/2")
                ustc2seq.emplace(sequenceNumber);
            if (log_mask & LOG_REQ) {
                if (log_mask & LOG_TOFILE)
                    logstream << std::setiosflags(std::ios::left) << std::setprecision(12)
                    << "time," << std::setw(15) << Simulator::Now().GetSeconds()
                    << ",req,\t"
                    << ",name, " << m_interestName
                    << ",Window, " << std::setw(15) << m_window
                    << ",inFlight," << std::setw(15) << m_inFlight
                    << ",seq," << std::setw(15) << sequenceNumber
                    << std::endl;

                else
                    std::cout << std::setiosflags(std::ios::left) << std::setprecision(12)
                    << "time," << std::setw(15) << Simulator::Now().GetSeconds()
                    << ",req,\t"
                    << ",name, " << m_interestName
                    << ",Window, " << std::setw(15) << m_window
                    << ",inFlight," << std::setw(15) << m_inFlight
                    << ",seq," << std::setw(15) << sequenceNumber
                    << std::endl;
            }
            ConsumerWindow::WillSendOutInterest(sequenceNumber);
        }

        void ConsumerNE::SetRandomPrefix(std::string random_prefix)
        {
            if (!random_prefix.empty()) {
                double acml = 0;
                std::size_t bpos = 0, epos = 0;
                do {
                    epos = random_prefix.find(',', bpos);
                    std::string kvpair = random_prefix.substr(bpos, epos - bpos);
                    bpos = epos + 1;
                    acml += std::stod(kvpair.substr(kvpair.find('=') + 1));
                    intervalp.push_back(acml);
                    intervalmap.emplace(std::make_pair(acml, kvpair.substr(0, kvpair.find('='))));
                } while (bpos != std::string::npos + 1);
                randprefix = true;
            }
            else
                randprefix = false;
        }
    }
}
