//#define LOG_TIMEOUT
//#define LOG_NACK
#include "consumerCCs.h"
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/ndnSIM-module.h"
#include "ns3/ndnSIM/helper/ndn-link-control-helper.hpp"
#include "ns3/ptr.h"
#include "string"
#include "random"
double globalbw=0;


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

        //Set ID and PoolSize of shared memory(shm) of ns3-ai
        Config::SetGlobalFailSafe("SharedMemoryKey", UintegerValue(1234));
        Config::SetGlobalFailSafe("SharedMemoryPoolSize", UintegerValue(1040));

        //Use system entropy source and mersenne twister engine
        std::random_device rdev;
        //Randomize initial window
        std::mt19937 reng(rdev());
        std::uniform_int_distribution<> u0(1, 10);
        string str = std::to_string(u0(reng));
        //Randomize seed
        reng.seed(rdev());
        std::uniform_int_distribution<> u1(0);
        ns3::SeedManager smgr;
        smgr.SetSeed(u1(reng));
        //Ransomize BW
        reng.seed(rdev());
        std::uniform_int_distribution<> u2(25, 50);

        CommandLine cmd;
        cmd.Parse(argc, argv);

        AnnotatedTopologyReader topologyReader("", 15);
        topologyReader.SetFileName("/root/ndn/proj-sep/scenarios/topo_baseline.txt");
        topologyReader.Read();
        NodeContainer allNodes = topologyReader.GetNodes();
        Ptr<Node> c0 = allNodes[0];
        Ptr<Node> r0 = allNodes[1];
        Ptr<Node> r1 = allNodes[2];
        Ptr<Node> p0 = allNodes[3];
        //ns3::ChannelList allLinks;
        //for (int i = 0;i < allLinks.GetNChannels();i++) {
        //    Ptr<ns3::PointToPointChannel> p2plink = StaticCast<ns3::PointToPointChannel>(allLinks.GetChannel(i));
        //    string randBW = to_string(u2(reng)) + "Mbps";
        //    for (int i = 0;i < p2plink->GetNDevices();i++) {
        //        auto device = p2plink->GetDevice(i);
        //        if (device->SetAttributeFailSafe("DataRate", StringValue(randBW)))
        //            std::cout << "set link-" << p2plink->GetId() << " device-" << device << " BW-" << randBW << std::endl;
        //    }
        //}


        // Install NDN stack on all nodes
        ndn::StackHelper ndnHelper;
        //ndnHelper.SetDefaultRoutes(true);
        ndnHelper.InstallAll();

        // Routing strategy
        ndn::GlobalRoutingHelper ndnGlobalRoutingHelper;
        ndnGlobalRoutingHelper.InstallAll();
        ndnGlobalRoutingHelper.AddOrigins("/ustc", p0);
        ndnGlobalRoutingHelper.CalculateRoutes();

        // Forwarding strategy
        //ndn::StrategyChoiceHelper::Install(allNodes[3], "/ustc", "/localhost/nfd/strategy/best-route2-conges/%FD%01");
        //ndn::StrategyChoiceHelper::Install(allNodes[4], "/ustc", "/localhost/nfd/strategy/best-route2-conges/%FD%01");
        ndn::StrategyChoiceHelper::Install(allNodes[1], "/ustc", "/localhost/nfd/strategy/best-route/%FD%05");
        ndn::StrategyChoiceHelper::Install(allNodes[2], "/ustc", "/localhost/nfd/strategy/best-route/%FD%05");
        ndn::StrategyChoiceHelper::Install(c0, "/ustc", "/localhost/nfd/strategy/best-route/%FD%05");
        ndn::StrategyChoiceHelper::Install(p0, "/ustc", "/localhost/nfd/strategy/best-route/%FD%05");

        // Installing Consumer
        ndn::AppHelper consumerHelper("ns3::ndn::ConsumerCCs");
        consumerHelper.SetPrefix("/ustc");
        consumerHelper.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper.SetAttribute("Window", StringValue("2"));
        consumerHelper.SetAttribute("CcAlgorithm", EnumValue(ndn::CCType::RL));
        consumerHelper.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper.SetAttribute("Frequency", DoubleValue(0));
        consumerHelper.SetAttribute("Randomize", StringValue("none"));
        consumerHelper.SetAttribute("WatchDog", DoubleValue(0.2));
        consumerHelper.Install(c0);

        // Installing Producer
        ndn::AppHelper producerHelper("ns3::ndn::Producer");
        producerHelper.SetPrefix("/ustc");
        producerHelper.SetAttribute("PayloadSize", StringValue("1024"));
        producerHelper.Install(p0);

        //Simulator::Stop(Seconds(60));
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
