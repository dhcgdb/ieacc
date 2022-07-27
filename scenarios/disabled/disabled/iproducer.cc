#include "iproducer.h"
#include "ns3/log.h"
#include "ns3/string.h"
#include "ns3/uinteger.h"
#include "ns3/packet.h"
#include "ns3/simulator.h"
#include "ndnSIM/model/ndn-l3-protocol.hpp"
#include "ndnSIM/helper/ndn-fib-helper.hpp"
#include <memory>

NS_LOG_COMPONENT_DEFINE("ndn.iProducer");

namespace ns3 {
    namespace ndn {

        NS_OBJECT_ENSURE_REGISTERED(iProducer);

        TypeId iProducer::GetTypeId(void)
        {
            static TypeId tid =
                TypeId("ns3::ndn::iProducer")
                .SetGroupName("Ndn")
                .SetParent<App>()
                .AddConstructor<iProducer>()
                .AddAttribute("Prefix", "Prefix, for which iProducer has the data",
                              StringValue("/"),
                              MakeNameAccessor(&iProducer::m_prefix),
                              MakeNameChecker())
                .AddAttribute("Postfix", "Postfix that is added to the output data (e.g., for adding iProducer-uniqueness)",
                              StringValue("/"),
                              MakeNameAccessor(&iProducer::m_postfix),
                              MakeNameChecker())
                .AddAttribute("PayloadSize", "Virtual payload size for Content packets",
                              UintegerValue(1024),
                              MakeUintegerAccessor(&iProducer::m_virtualPayloadSize),
                              MakeUintegerChecker<uint32_t>())
                .AddAttribute("Freshness", "Freshness of data packets, if 0, then unlimited freshness",
                              TimeValue(Seconds(0)),
                              MakeTimeAccessor(&iProducer::m_freshness),
                              MakeTimeChecker())
                .AddAttribute("Signature", "Fake signature, 0 valid signature (default), other values application-specific",
                              UintegerValue(0),
                              MakeUintegerAccessor(&iProducer::m_signature),
                              MakeUintegerChecker<uint32_t>())
                .AddAttribute("KeyLocator", "Name to be used for key locator.  If root, then key locator is not used",
                              NameValue(),
                              MakeNameAccessor(&iProducer::m_keyLocator),
                              MakeNameChecker());
            return tid;
        }

        iProducer::iProducer()
        {
            NS_LOG_FUNCTION_NOARGS();
        }

        // inherited from Application base class.
        void
            iProducer::StartApplication()
        {
            NS_LOG_FUNCTION_NOARGS();
            App::StartApplication();

            FibHelper::AddRoute(GetNode(), m_prefix, m_face, 0);
        }

        void
            iProducer::StopApplication()
        {
            NS_LOG_FUNCTION_NOARGS();

            App::StopApplication();
        }

        void
            iProducer::OnInterest(shared_ptr<const Interest> interest)
        {
            App::OnInterest(interest); // tracing inside

            NS_LOG_FUNCTION(this << interest);

            if (!m_active)
                return;

            Name dataName(interest->getName());
            dataName.append(m_postfix);
            // dataName.appendVersion();

            auto data = make_shared<Data>();
            data->setName(dataName);
            data->setFreshnessPeriod(::ndn::time::milliseconds(m_freshness.GetMilliSeconds()));

            data->setContent(make_shared< ::ndn::Buffer>(m_virtualPayloadSize));

            Signature signature;
            SignatureInfo signatureInfo(static_cast<::ndn::tlv::SignatureTypeValue>(255));

            if (m_keyLocator.size() > 0) {
                signatureInfo.setKeyLocator(m_keyLocator);
            }

            signature.setInfo(signatureInfo);
            signature.setValue(::ndn::makeNonNegativeIntegerBlock(::ndn::tlv::SignatureValue, m_signature));

            data->setSignature(signature);



            NS_LOG_INFO("node(" << GetNode()->GetId() << ") responding with Data: " << data->getName());

            // to create real wire encoding
            data->wireEncode();

            m_transmittedDatas(data, this, m_face);
            m_appLink->onReceiveData(*data);
        }

    } // namespace ndn
} // namespace ns3
