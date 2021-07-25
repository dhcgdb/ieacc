#include "proj0.h"

NS_LOG_COMPONENT_DEFINE("ndn.ConsumerRLCtrl");

namespace ns3 {
    TransParam2Py::TransParam2Py(uint16_t id) :
        Ns3AIRL<DDPGParam, DDPGAct>(id) {
        SetCond(2, 0);
    }

    namespace ndn {
        NS_OBJECT_ENSURE_REGISTERED(ConsumerRLCtrl);

        TypeId ConsumerRLCtrl::GetTypeId(void) {
            static TypeId tid =
                TypeId("ns3::ndn::ConsumerRLCtrl")
                .SetGroupName("Ndn")
                .SetParent<Consumer>()
                .AddConstructor<ConsumerRLCtrl>()
                .AddAttribute("Frequency", "Frequency of interest packets", StringValue("10"),
                    MakeDoubleAccessor(&ConsumerRLCtrl::m_frequency), MakeDoubleChecker<double>())
                .AddAttribute("Randomize",
                    "Type of send time randomization: none (default), uniform, exponential",
                    StringValue("none"),
                    MakeStringAccessor(&ConsumerRLCtrl::SetRandomize, &ConsumerRLCtrl::GetRandomize),
                    MakeStringChecker())
                .AddAttribute("MaxSeq", "Maximum sequence number to request",
                    IntegerValue(std::numeric_limits<uint32_t>::max()),
                    MakeIntegerAccessor(&ConsumerRLCtrl::m_seqMax), MakeIntegerChecker<uint32_t>());
            return tid;
        }

        ConsumerRLCtrl::ConsumerRLCtrl() :
            m_frequency(10), m_firstTime(true), cWnd(3), cWnd_scale(3),
            minRTO(0.1), avgDelay(1.0), interestsInFlight(0), Nloss(0), Rloss(0) {
            NS_LOG_FUNCTION_NOARGS();
            m_seqMax = std::numeric_limits<uint32_t>::max();
            transclass = Create<TransParam2Py>(1024);
        }

        ConsumerRLCtrl::~ConsumerRLCtrl() {}

        void ConsumerRLCtrl::ScheduleNextPacket() {
            // double mean = 8.0 * m_payloadSize / m_desiredRate.GetBitRate ();
            // std::cout << "next: " << Simulator::Now().ToDouble(Time::S) + mean << "s\n";
            if (m_firstTime) {
                m_sendEvent = Simulator::Schedule(Seconds(0.0), &Consumer::SendPacket, this);
                m_firstTime = false;
            }
            else if (!m_sendEvent.IsRunning()) {
                if (0 == static_cast<uint32_t>(cWnd)) {
                }
                else if (interestsInFlight >= static_cast<uint32_t>(cWnd)) {
                }
                else {
                    m_sendEvent = Simulator::Schedule((m_random == 0) ? Seconds(1.0 / m_frequency)
                        : Seconds(m_random->GetValue()),
                        &Consumer::SendPacket, this);
                }
            }
        }

        void ConsumerRLCtrl::OnData(shared_ptr<const Data> contentObject) {
            Consumer::OnData(contentObject);//Data包到来时调用Consumer默认实现方式更新rtt、等待队列等

            //更新参数
            minRTO = m_rtt->GetMinRto().GetSeconds();
            avgDelay = m_rtt->GetCurrentEstimate().GetSeconds();
            interestsInFlight = Consumer::m_seqTimeouts.size();
            NS_LOG_DEBUG("cWnd:" << cWnd << ", minRTO:" << minRTO << ", avgDelay:" << avgDelay << \
                ", InFlight:" << interestsInFlight << ", Nloss:" << Nloss << ", Rloss:" << Rloss);
            //调节窗口
            SendParam2RLModule();
            GetRetFromRLModule();
            cWnd = cWnd_scale < 3 ? 3 : cWnd_scale;
            //
            ScheduleNextPacket();
        }

        //Consumer没有实现OnNack的动作，我自己理解一下实现了一个
        void ConsumerRLCtrl::OnNack(shared_ptr<const lp::Nack> nack) {
            Consumer::OnNack(nack);
            if (nack->getReason() == lp::NackReason::CONGESTION) {
                uint32_t seqnum = nack->getInterest().getName().at(-1).toSequenceNumber();
                m_seqTimeouts.erase(seqnum);
                //m_seqFullDelay.erase(seqnum);
                m_rtt->SentSeq(SequenceNumber32(seqnum), 1);
                m_retxSeqs.insert(seqnum);

                //更新参数
                minRTO = m_rtt->GetMinRto().GetSeconds();
                avgDelay = m_rtt->GetCurrentEstimate().GetSeconds();
                interestsInFlight = Consumer::m_seqTimeouts.size();
                Nloss++;
                NS_LOG_DEBUG("cWnd:" << cWnd << ", minRTO:" << minRTO << ", avgDelay:" << avgDelay << \
                    ", InFlight:" << interestsInFlight << ", Nloss:" << Nloss << ", Rloss:" << Rloss);
                //调节窗口
                SendParam2RLModule();
                GetRetFromRLModule();
                cWnd = cWnd_scale < 3 ? 3 : cWnd_scale;
                //

                ScheduleNextPacket();//拥塞导致的Nack则尝试进行重发
            }
        }

        void ConsumerRLCtrl::OnTimeout(uint32_t sequenceNumber)
        {
            NS_LOG_FUNCTION(sequenceNumber);
            m_rtt->IncreaseMultiplier();
            m_rtt->SentSeq(SequenceNumber32(sequenceNumber), 1);
            m_retxSeqs.insert(sequenceNumber);

            //更新参数
            minRTO = m_rtt->GetMinRto().GetSeconds();
            avgDelay = m_rtt->GetCurrentEstimate().GetSeconds();
            interestsInFlight = Consumer::m_seqTimeouts.size();
            Rloss++;
            NS_LOG_DEBUG("cWnd:" << cWnd << ", minRTO:" << minRTO << ", avgDelay:" << avgDelay << \
                ", InFlight:" << interestsInFlight << ", Nloss:" << Nloss << ", Rloss:" << Rloss);
            //调节窗口
            SendParam2RLModule();
            GetRetFromRLModule();
            cWnd = cWnd_scale < 3 ? 3 : cWnd_scale;
            //

            ScheduleNextPacket();//尝试重发超时包
        }

        void ConsumerRLCtrl::SetRandomize(const std::string& value)
        {
            if (value == "uniform") {
                m_random = CreateObject<UniformRandomVariable>();
                m_random->SetAttribute("Min", DoubleValue(0.0));
                m_random->SetAttribute("Max", DoubleValue(2 * 1.0 / m_frequency));
            }
            else if (value == "exponential") {
                m_random = CreateObject<ExponentialRandomVariable>();
                m_random->SetAttribute("Mean", DoubleValue(1.0 / m_frequency));
                m_random->SetAttribute("Bound", DoubleValue(50 * 1.0 / m_frequency));
            }
            else
                m_random = 0;

            m_randomType = value;
        }

        std::string ConsumerRLCtrl::GetRandomize() const
        {
            return m_randomType;
        }

        void ConsumerRLCtrl::SendParam2RLModule() {
            auto shm_send = transclass->EnvSetterCond();
            shm_send->cWnd = cWnd;
            shm_send->avgDelay = avgDelay;
            shm_send->interestsInFlight = interestsInFlight;
            shm_send->minRTO = minRTO;
            shm_send->Nloss = Nloss;
            shm_send->Rloss = Rloss;
            transclass->SetCompleted();
        }

        void ConsumerRLCtrl::GetRetFromRLModule() {
            auto shm_recv = transclass->ActionGetterCond();
            cWnd_scale = shm_recv->wnd_scale;
            transclass->GetCompleted();
        }

    }
}
