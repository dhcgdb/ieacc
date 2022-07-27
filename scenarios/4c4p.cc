#include "consumerCCs.h"
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/ndnSIM-module.h"
#include "string"
#include "random"
#define LOG_DATA 0b1
#define LOG_TIMEOUT 0b10
#define LOG_NACK 0b100
#define LOG_LEARNING 0b1000
double globalbw=0;

namespace ns3 {
    int main(int argc, char* argv[])
    {
        Config::SetGlobalFailSafe("SharedMemoryKey", UintegerValue(128));
        Config::SetGlobalFailSafe("SharedMemoryPoolSize", UintegerValue(1040));

        std::random_device rdev;
        std::mt19937 reng(rdev());
        std::uniform_int_distribution<> u(1, 10);
        std::uniform_int_distribution<> uuu(0);
        const string str = std::to_string(u(reng));
        ns3::SeedManager smgr;
        smgr.SetSeed(uuu(reng));

        CommandLine cmd;
        cmd.Parse(argc, argv);


        AnnotatedTopologyReader topologyReader("", 15);
        topologyReader.SetFileName("/root/ndn/proj-sep/scenarios/topo_tree.txt");
        topologyReader.Read();
        NodeContainer allNodes = topologyReader.GetNodes();
        Ptr<Node> rootc0 = allNodes[0];
        Ptr<Node> l1n0 = allNodes[1];
        Ptr<Node> l1n1 = allNodes[2];
        Ptr<Node> l2n0 = allNodes[3];
        Ptr<Node> l2n1p1 = allNodes[4];
        Ptr<Node> l2n2p2 = allNodes[5];
        Ptr<Node> l2n3p3 = allNodes[6];
        Ptr<Node> l3n0p0 = allNodes[7];

        // Install NDN stack on all nodes
        ndn::StackHelper ndnHelper;
        //ndnHelper.SetDefaultRoutes(true);
        ndnHelper.InstallAll();

        // Routing strategy
        ndn::GlobalRoutingHelper ndnGlobalRoutingHelper;
        ndnGlobalRoutingHelper.InstallAll();
        ndnGlobalRoutingHelper.AddOrigin("/ustc/0", l3n0p0);
        ndnGlobalRoutingHelper.AddOrigin("/ustc/1", l2n1p1);
        ndnGlobalRoutingHelper.AddOrigin("/ustc/2", l2n2p2);
        ndnGlobalRoutingHelper.AddOrigin("/ustc/3", l2n3p3);
        //ndnGlobalRoutingHelper.CalculateAllPossibleRoutes();
        ndnGlobalRoutingHelper.CalculateLfidRoutes();
        //ndnGlobalRoutingHelper.CalculateRoutes();

        // Forwarding strategy
        ndn::StrategyChoiceHelper::InstallAll("/ustc", "/localhost/nfd/strategy/best-route/%FD%05");

        // Installing Consumer
        ndn::AppHelper consumerHelper0("ns3::ndn::ConsumerCCs");
        consumerHelper0.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper0.SetAttribute("Window", StringValue("4"));
        consumerHelper0.SetAttribute("CcAlgorithm", EnumValue(ndn::CCType::RL));
        consumerHelper0.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper0.SetAttribute("Frequency", DoubleValue(0));
        consumerHelper0.SetAttribute("Randomize", StringValue("none"));
        consumerHelper0.SetAttribute("WatchDog", DoubleValue(0.2));
        consumerHelper0.SetAttribute("LogMask", IntegerValue(LOG_LEARNING));
        consumerHelper0.SetAttribute("ShmID", IntegerValue(1024));
        consumerHelper0.SetPrefix("/ustc/0");
        consumerHelper0.Install(rootc0);

        ndn::AppHelper consumerHelper1("ns3::ndn::ConsumerCCs");
        consumerHelper1.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper1.SetAttribute("Window", StringValue("4"));
        consumerHelper1.SetAttribute("CcAlgorithm", EnumValue(ndn::CCType::AIMD));
        consumerHelper1.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper1.SetAttribute("Frequency", DoubleValue(0));
        consumerHelper1.SetAttribute("Randomize", StringValue("none"));
        consumerHelper1.SetAttribute("WatchDog", DoubleValue(0));
        consumerHelper1.SetAttribute("ShmID", IntegerValue(1050));
        consumerHelper1.SetPrefix("/ustc/1");
        consumerHelper1.Install(rootc0);

        ndn::AppHelper consumerHelper2("ns3::ndn::ConsumerCCs");
        consumerHelper2.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper2.SetAttribute("Window", StringValue("4"));
        consumerHelper2.SetAttribute("CcAlgorithm", EnumValue(ndn::CCType::AIMD));
        consumerHelper2.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper2.SetAttribute("Frequency", DoubleValue(0));
        consumerHelper2.SetAttribute("Randomize", StringValue("none"));
        consumerHelper2.SetAttribute("WatchDog", DoubleValue(0));
        consumerHelper2.SetPrefix("/ustc/2");
        consumerHelper2.Install(rootc0);

        ndn::AppHelper consumerHelper3("ns3::ndn::ConsumerCCs");
        consumerHelper3.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper3.SetAttribute("Window", StringValue("4"));
        consumerHelper3.SetAttribute("CcAlgorithm", EnumValue(ndn::CCType::AIMD));
        consumerHelper3.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper3.SetAttribute("Frequency", DoubleValue(0));
        consumerHelper3.SetAttribute("Randomize", StringValue("none"));
        consumerHelper3.SetAttribute("WatchDog", DoubleValue(0));
        consumerHelper3.SetPrefix("/ustc/3");
        consumerHelper3.Install(rootc0);


        // Installing Producer
        ndn::AppHelper producerHelper0("ns3::ndn::Producer");
        producerHelper0.SetAttribute("PayloadSize", StringValue("1024"));
        producerHelper0.SetPrefix("/ustc/0");
        producerHelper0.Install(l3n0p0);

        ndn::AppHelper producerHelper1("ns3::ndn::Producer");
        producerHelper1.SetAttribute("PayloadSize", StringValue("1024"));
        producerHelper1.SetPrefix("/ustc/1");
        producerHelper1.Install(l2n1p1);

        ndn::AppHelper producerHelper2("ns3::ndn::Producer");
        producerHelper2.SetAttribute("PayloadSize", StringValue("1024"));
        producerHelper2.SetPrefix("/ustc/2");
        producerHelper2.Install(l2n2p2);

        ndn::AppHelper producerHelper3("ns3::ndn::Producer");
        producerHelper3.SetAttribute("PayloadSize", StringValue("1024"));
        producerHelper3.SetPrefix("/ustc/3");
        producerHelper3.Install(l2n3p3);

        //Simulator::Stop(Seconds(200));
        Simulator::Run();
        Simulator::Destroy();
        return 0;
    }

} // namespace ns3

int
main(int argc, char* argv[])
{
    return ns3::main(argc, argv);
}
