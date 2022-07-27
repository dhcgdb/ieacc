#include "ndnSIM/model/ndn-common.hpp"

#include "ndnSIM/apps/ndn-app.hpp"
#include "ndnSIM/model/ndn-common.hpp"

#include "nstime.h"
#include "ptr.h"

namespace ns3 {
    namespace ndn {


        class iProducer : public App {
        public:
            static TypeId
                GetTypeId(void);

            iProducer();

            virtual void OnInterest(shared_ptr<const Interest> interest);

        protected:
            virtual void StartApplication();
            virtual void StopApplication();
        private:
            Name m_prefix;
            Name m_postfix;
            uint32_t m_virtualPayloadSize;
            Time m_freshness;

            uint32_t m_signature;
            Name m_keyLocator;
        };

    } // namespace ndn
} // namespace ns3

