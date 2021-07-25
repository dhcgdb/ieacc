#include "ns3/ndnSIM/model/ndn-common.hpp"
#include "ns3/ns3-ai-module.h"
#include "ns3/ndnSIM/apps/ndn-consumer.hpp"
#include "ns3/ndnSIM/apps/ndn-consumer-pcon.hpp"
#include "ns3/ptr.h"
#include "ns3/ptr.h"
#include "ns3/log.h"
#include "ns3/simulator.h"
#include "ns3/packet.h"
#include "ns3/callback.h"
#include "ns3/string.h"
#include "ns3/boolean.h"
#include "ns3/uinteger.h"
#include "ns3/integer.h"
#include "ns3/double.h"

namespace ns3 {
    struct DDPGParam {
        double cWnd;
        double minRTO;
        double avgDelay;
        uint32_t interestsInFlight;
        uint32_t Nloss;
        uint32_t Rloss;
        //int32_t datasize;
    }Packed;

    struct DDPGAct {
        double wnd_scale;
    }Packed;

    class TransParam2Py : public Ns3AIRL<DDPGParam, DDPGAct> {
    public:
        TransParam2Py(uint16_t id);
    };

    namespace ndn {
        class ConsumerRLCtrl : public ConsumerWindow {
        public:
            static TypeId GetTypeId();
            ConsumerRLCtrl();
            virtual ~ConsumerRLCtrl();

        protected:
            virtual void ScheduleNextPacket();

            virtual void OnData(shared_ptr<const Data> contentObject);

            virtual void OnNack(shared_ptr<const lp::Nack> nack);

            virtual void OnTimeout(uint32_t sequenceNumber);
            
            //'none', 'uniform', or 'exponential'
            void SetRandomize(const std::string& value);
            std::string GetRandomize() const;

        private:
            void SendParam2RLModule();
            void GetRetFromRLModule();

        protected:
            double m_frequency; // Frequency of interest packets (in hertz)
            bool m_firstTime;
            Ptr<RandomVariableStream> m_random;
            std::string m_randomType;


        private:
            Ptr<TransParam2Py> transclass;
            double cWnd_scale;

            double  cWnd;
            double  minRTO;
            double  avgDelay;
            uint32_t interestsInFlight;
            uint32_t Nloss;
            uint32_t Rloss;
        };

    } // namespace ndn
} // namespace ns3
