#include "consumerNE.h"
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/ndnSIM-module.h"
#include "ns3/ndnSIM/helper/ndn-link-control-helper.hpp"
#include "ns3/ptr.h"
#include "string"
#include "random"
#define LOG_DATA 0b1
#define LOG_TIMEOUT 0b10
#define LOG_NACK 0b100
#define LOG_LEARNING 0b1000
#define LOG_REQ 0b10000

double globalbw=0;

namespace ns3 {
    void changeBWFunc(Ptr<Node> n0, Ptr<Node> n1, int cur_BW, const int to_BW, Watchdog* wd)
    {
        if (cur_BW > to_BW)
            cur_BW -= 1;
        else if (cur_BW < to_BW)
            cur_BW += 1;
        else
            return;

        std::random_device rdev;
        std::mt19937 reng(rdev());
        std::uniform_int_distribution<> u2(25, 50);
        ChannelList allLinks;
        for (int i = 0;i < allLinks.GetNChannels();i++) {
            Ptr<ns3::PointToPointChannel> p2plink = StaticCast<ns3::PointToPointChannel>(allLinks.GetChannel(i));
            if (p2plink->GetNDevices() != 2)
                continue;
            auto dev0 = p2plink->GetDevice(0), dev1 = p2plink->GetDevice(1);
            if ((dev0->GetNode() == n0 && dev1->GetNode() == n1) || (dev0->GetNode() == n1 && dev1->GetNode() == n0)) {
                string randBW = to_string(cur_BW) + "Mbps";
                if (dev0->SetAttributeFailSafe("DataRate", StringValue(randBW))) {
                    std::cout << ns3::Simulator::Now().GetSeconds() << std::endl;
                    std::cout << "\033[31;43m" << "set link-" << p2plink->GetId() << " device-" << dev0 << " BW-" << randBW << "\033[0m" << std::endl;
                }
                if (dev1->SetAttributeFailSafe("DataRate", StringValue(randBW)))
                    std::cout << "\033[31;43m" << "set link-" << p2plink->GetId() << " device-" << dev1 << " BW-" << randBW << "\033[0m" << std::endl;
            }
        }
        globalbw=cur_BW;
        wd->Ping(Seconds(0.1));
        wd->SetArguments(n0, n1, cur_BW, to_BW, wd);
    }

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
        topologyReader.SetFileName("/root/ndn/proj-sep/scenarios/topo_2p.txt");
        topologyReader.Read();
        NodeContainer allNodes = topologyReader.GetNodes();
        Ptr<Node> c0 = allNodes[0];
        Ptr<Node> p0 = allNodes[1];
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
        ndn::StrategyChoiceHelper::Install(c0, "/ustc", "/localhost/nfd/strategy/best-route/%FD%05");
        ndn::StrategyChoiceHelper::Install(p0, "/ustc", "/localhost/nfd/strategy/best-route/%FD%05");

        int startime[] = { 0,20,30,60 };
        int endtime[] = { 40,60,75,80 };
        // Installing Consumer
        for (int i = 0;i < 2;i++) {
            ndn::AppHelper consumerHelper("ns3::ndn::ConsumerNE");
            consumerHelper.SetPrefix("/ustc");
            consumerHelper.SetAttribute("RetxTimer", StringValue("10ms"));
            consumerHelper.SetAttribute("Window", StringValue("2"));
            consumerHelper.SetAttribute("CcAlgorithm", EnumValue(ndn::CCType::RL));
            consumerHelper.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
            consumerHelper.SetAttribute("Frequency", DoubleValue(0));
            consumerHelper.SetAttribute("Randomize", StringValue("none"));
            consumerHelper.SetAttribute("WatchDog", DoubleValue(0.2));
            consumerHelper.SetAttribute("LogMask", IntegerValue(LOG_DATA | LOG_NACK | LOG_TIMEOUT | LOG_LEARNING | LOG_REQ));
            consumerHelper.SetAttribute("Log2File", StringValue("/root/ndn/proj-sep/log/multiport/nec-" + std::to_string(i) + ".log"));
            consumerHelper.SetAttribute("ShmID", IntegerValue(500 + i));
            consumerHelper.SetAttribute("RandomPrefix", StringValue(""));
            auto appptr = consumerHelper.Install(c0);
            appptr.Get(0)->SetStartTime(Seconds(startime[i]));
            appptr.Get(0)->SetStopTime(Seconds(endtime[i]));
        }

        // Installing Producer
        ndn::AppHelper producerHelper("ns3::ndn::Producer");
        producerHelper.SetPrefix("/ustc");
        producerHelper.SetAttribute("PayloadSize", StringValue("1024"));
        producerHelper.Install(p0);

        int BWs[] = { 50,70,60,40 };
        double TPs[] = { 0,20,40,60 };
        globalbw=BWs[0];
        Watchdog changeBW[20];
        for (int i = 0;i < sizeof(BWs) / 4 - 1;i++) {
            //changeBW[i].Ping(Seconds(TPs[i + 1]));
            changeBW[i].SetFunction(changeBWFunc);
            changeBW[i].SetArguments(c0, p0, BWs[i], BWs[i + 1], &changeBW[i]);
        }

        Simulator::Stop(Seconds(60));
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
