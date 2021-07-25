#include "rl.h"
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/ndnSIM-module.h"
#include "string"
#include "random"


namespace ns3 {
    int main(int argc, char* argv[])
    {
        /*
        // setting default parameters for PointToPoint links and channels
        Config::SetDefault("ns3::PointToPointNetDevice::DataRate", StringValue("2Mbps"));
        Config::SetDefault("ns3::PointToPointChannel::Delay", StringValue("10ms"));
        Config::SetDefault("ns3::QueueBase::MaxSize", StringValue("20p"));
        // Creating nodes
        NodeContainer nodes;
        nodes.Create(3);
        // Connecting nodes using two links
        PointToPointHelper p2p;
        p2p.Install(nodes.Get(0), nodes.Get(1));
        p2p.Install(nodes.Get(1), nodes.Get(2));
        */
        // Read optional command-line parameters (e.g., enable visualizer with ./waf --run=<> --visualize
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
        topologyReader.SetFileName("/root/ndnproj/scenarios/topo_multiport.txt");
        topologyReader.Read();
        NodeContainer allNodes = topologyReader.GetNodes();
        Ptr<Node> c0 = allNodes[0];
        Ptr<Node> p0 = allNodes[1];
        Ptr<Node> p1 = allNodes[2];
        Ptr<Node> p2 = allNodes[3];
        Ptr<Node> n0 = allNodes[4];
        Ptr<Node> n1 = allNodes[5];
        Ptr<Node> n2 = allNodes[6];
        Ptr<Node> n3 = allNodes[7];

        // Install NDN stack on all nodes
        ndn::StackHelper ndnHelper;
        //ndnHelper.SetDefaultRoutes(true);
        ndnHelper.InstallAll();

        // Routing strategy
        ndn::GlobalRoutingHelper ndnGlobalRoutingHelper;
        ndnGlobalRoutingHelper.InstallAll();
        ndnGlobalRoutingHelper.AddOrigins("/ustc/0", p0);
        ndnGlobalRoutingHelper.AddOrigins("/ustc/1", p1);
        ndnGlobalRoutingHelper.AddOrigins("/ustc/2", p2);
        //ndnGlobalRoutingHelper.CalculateAllPossibleRoutes();
        //ndnGlobalRoutingHelper.CalculateLfidRoutes();
        ndnGlobalRoutingHelper.CalculateRoutes();

        // Forwarding strategy
        //ndn::StrategyChoiceHelper::Install(n0, "/ustc", "/localhost/nfd/strategy/best-route2-conges/%FD%01");
        ndn::StrategyChoiceHelper::Install(n0, "/ustc", "/localhost/nfd/strategy/best-route");
        ndn::StrategyChoiceHelper::Install(n1, "/ustc", "/localhost/nfd/strategy/best-route");
        ndn::StrategyChoiceHelper::Install(n2, "/ustc", "/localhost/nfd/strategy/best-route");
        ndn::StrategyChoiceHelper::Install(n3, "/ustc", "/localhost/nfd/strategy/best-route2-conges-multiport/%FD%01");
        ndn::StrategyChoiceHelper::Install(c0, "/ustc", "/localhost/nfd/strategy/best-route");
        ndn::StrategyChoiceHelper::Install(p0, "/ustc", "/localhost/nfd/strategy/best-route");
        ndn::StrategyChoiceHelper::Install(p1, "/ustc", "/localhost/nfd/strategy/best-route");
        ndn::StrategyChoiceHelper::Install(p2, "/ustc", "/localhost/nfd/strategy/best-route");

        // Installing Consumer
        ndn::AppHelper consumerHelper0("ns3::ndn::ConsumerRL");
        consumerHelper0.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper0.SetAttribute("Window", StringValue("4"));
        consumerHelper0.SetAttribute("CcAlgorithm", EnumValue(ndn::CcAlgorithm::AIMD));
        consumerHelper0.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper0.SetAttribute("Frequency", DoubleValue(65536));
        consumerHelper0.SetAttribute("Randomize", StringValue("exponential"));
        consumerHelper0.SetAttribute("WatchDog", DoubleValue(0));
        //consumerHelper0.SetAttribute("RandomPrefix",BooleanValue(true));
        consumerHelper0.SetPrefix("/ustc/0");
        consumerHelper0.Install(c0);

        ndn::AppHelper consumerHelper1("ns3::ndn::ConsumerRL");
        consumerHelper1.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper1.SetAttribute("Window", StringValue("4"));
        consumerHelper1.SetAttribute("CcAlgorithm", EnumValue(ndn::CcAlgorithm::AIMD));
        consumerHelper1.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper1.SetAttribute("Frequency", DoubleValue(65536));
        consumerHelper1.SetAttribute("Randomize", StringValue("exponential"));
        consumerHelper1.SetAttribute("WatchDog", DoubleValue(0));
        consumerHelper1.SetPrefix("/ustc/1");
        consumerHelper1.Install(c0);

        ndn::AppHelper consumerHelper2("ns3::ndn::ConsumerRL");
        consumerHelper2.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper2.SetAttribute("Window", StringValue("4"));
        consumerHelper2.SetAttribute("CcAlgorithm", EnumValue(ndn::CcAlgorithm::AIMD));
        consumerHelper2.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper2.SetAttribute("Frequency", DoubleValue(65536));
        consumerHelper2.SetAttribute("Randomize", StringValue("exponential"));
        consumerHelper2.SetAttribute("WatchDog", DoubleValue(0));
        consumerHelper2.SetPrefix("/ustc/2");
        consumerHelper2.Install(c0);
        
        // Installing Producer
        ndn::AppHelper producerHelper0("ns3::ndn::Producer");
        producerHelper0.SetAttribute("PayloadSize", StringValue("1024"));
        producerHelper0.SetPrefix("/ustc/0");
        producerHelper0.Install(p0);

        ndn::AppHelper producerHelper1("ns3::ndn::Producer");
        producerHelper1.SetAttribute("PayloadSize", StringValue("1024"));
        producerHelper1.SetPrefix("/ustc/1");
        producerHelper1.Install(p1);

        ndn::AppHelper producerHelper2("ns3::ndn::Producer");
        producerHelper2.SetAttribute("PayloadSize", StringValue("1024"));
        producerHelper2.SetPrefix("/ustc/2");
        producerHelper2.Install(p2);


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
