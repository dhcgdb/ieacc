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
#define LOG_REQ 0b10000

double globalbw = 0;

namespace ns3
{

    void randfreqFunc(Ptr<Application> cmptr, Watchdog *wd)
    {
        static std::random_device rdev;
        static std::mt19937 reng(rdev());
        static std::uniform_real_distribution<> u(375, 500);
        auto freq = u(reng);
        if (cmptr->SetAttributeFailSafe("Frequency", DoubleValue(freq)))
            std::cout
                << "Set App=" << cmptr << "= Frequency to " << freq << std::endl;
        wd->Ping(Seconds(2));
        wd->SetArguments(cmptr, wd);
    }

    int main(int argc, char *argv[])
    {
        Config::SetGlobalFailSafe("SharedMemoryKey", UintegerValue(1234));
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
        topologyReader.SetFileName("/root/ndn/proj-sep/scenarios/topo_baseline.txt");
        topologyReader.Read();
        NodeContainer allNodes = topologyReader.GetNodes();
        Ptr<Node> c0 = allNodes[0];
        Ptr<Node> r0 = allNodes[1];
        Ptr<Node> r1 = allNodes[2];
        Ptr<Node> p0 = allNodes[3];

        ndn::StackHelper ndnHelper;
        ndnHelper.InstallAll();

        ndn::GlobalRoutingHelper ndnGlobalRoutingHelper;
        ndnGlobalRoutingHelper.InstallAll();
        ndnGlobalRoutingHelper.AddOrigin("/ustc", p0);
        //ndnGlobalRoutingHelper.CalculateAllPossibleRoutes();
        //ndnGlobalRoutingHelper.CalculateLfidRoutes();
        ndnGlobalRoutingHelper.CalculateRoutes();

        ndn::StrategyChoiceHelper::InstallAll("/ustc", "/localhost/nfd/strategy/best-route/%FD%05");

        ndn::AppHelper consumerHelper0("ns3::ndn::ConsumerCCs");
        consumerHelper0.SetPrefix("/ustc/0");
        consumerHelper0.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper0.SetAttribute("Window", StringValue("2"));
        consumerHelper0.SetAttribute("CcAlgorithm", EnumValue(ndn::CCType::RL));
        consumerHelper0.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper0.SetAttribute("Frequency", DoubleValue(15000));
        consumerHelper0.SetAttribute("Randomize", StringValue("none"));
        consumerHelper0.SetAttribute("WatchDog", DoubleValue(0.2));
        consumerHelper0.SetAttribute("LogMask", IntegerValue(LOG_DATA | LOG_NACK | LOG_TIMEOUT | LOG_LEARNING | LOG_REQ));
        consumerHelper0.SetAttribute("Log2File", StringValue("/root/ndn/proj-sep/log/spec/fair-3ddpg-0.log"));
        consumerHelper0.SetAttribute("ShmID", IntegerValue(500));
        consumerHelper0.SetAttribute("RandomPrefix", StringValue(""));
        consumerHelper0.Install(c0);

        ndn::AppHelper consumerHelper1("ns3::ndn::ConsumerCCs");
        consumerHelper1.SetPrefix("/ustc/1");
        consumerHelper1.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper1.SetAttribute("Window", StringValue("2"));
        consumerHelper1.SetAttribute("CcAlgorithm", EnumValue(ndn::CCType::RL));
        consumerHelper1.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper1.SetAttribute("Frequency", DoubleValue(15000));
        consumerHelper1.SetAttribute("Randomize", StringValue("none"));
        consumerHelper1.SetAttribute("WatchDog", DoubleValue(0.2));
        consumerHelper1.SetAttribute("LogMask", IntegerValue(LOG_DATA | LOG_NACK | LOG_TIMEOUT | LOG_LEARNING | LOG_REQ));
        consumerHelper1.SetAttribute("Log2File", StringValue("/root/ndn/proj-sep/log/spec/fair-3ddpg-1.log"));
        consumerHelper1.SetAttribute("ShmID", IntegerValue(501));
        consumerHelper1.SetAttribute("RandomPrefix", StringValue(""));
        consumerHelper1.Install(c0);

        ndn::AppHelper consumerHelper2("ns3::ndn::ConsumerCCs");
        consumerHelper2.SetPrefix("/ustc/203");
        consumerHelper2.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper2.SetAttribute("Window", StringValue("2"));
        consumerHelper2.SetAttribute("CcAlgorithm", EnumValue(ndn::CCType::RL));
        consumerHelper2.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper2.SetAttribute("Frequency", DoubleValue(15000));
        consumerHelper2.SetAttribute("Randomize", StringValue("none"));
        consumerHelper2.SetAttribute("WatchDog", DoubleValue(0.2));
        consumerHelper2.SetAttribute("LogMask", IntegerValue(LOG_DATA | LOG_NACK | LOG_TIMEOUT | LOG_LEARNING));
        consumerHelper2.SetAttribute("Log2File", StringValue("/root/ndn/proj-sep/log/spec/fair-3ddpg-2.log"));
        consumerHelper2.SetAttribute("ShmID", IntegerValue(502));
        consumerHelper2.SetAttribute("RandomPrefix", StringValue(""));
        consumerHelper2.Install(c0);

        ndn::AppHelper consumerHelper3("ns3::ndn::ConsumerCCs");
        consumerHelper3.SetPrefix("/ustc/bg");
        consumerHelper3.SetAttribute("RetxTimer", StringValue("10ms"));
        consumerHelper3.SetAttribute("Window", StringValue("100000"));
        consumerHelper3.SetAttribute("CcAlgorithm", EnumValue(ndn::CCType::none));
        consumerHelper3.SetAttribute("InitialWindowOnTimeout", BooleanValue(true));
        consumerHelper3.SetAttribute("Frequency", DoubleValue(300));
        consumerHelper3.SetAttribute("Randomize", StringValue("none"));
        consumerHelper3.SetAttribute("WatchDog", DoubleValue(0));
        //consumerHelper2.SetAttribute("LogMask", IntegerValue(LOG_DATA | LOG_NACK | LOG_TIMEOUT | LOG_LEARNING));
        //consumerHelper2.SetAttribute("ShmID", IntegerValue(502));
        consumerHelper3.SetAttribute("RandomPrefix", StringValue(""));
        //auto cm = consumerHelper3.Install(c0).Get(0);
        //Watchdog randfreq;
        //randfreq.Ping(Seconds(0));
        //randfreq.SetFunction(randfreqFunc);
        //randfreq.SetArguments(cm, &randfreq);

        ndn::AppHelper producerHelper0("ns3::ndn::Producer");
        producerHelper0.SetAttribute("PayloadSize", StringValue("1024"));
        producerHelper0.SetPrefix("/ustc");
        producerHelper0.Install(p0);

        Simulator::Stop(Seconds(60));
        Simulator::Run();
        Simulator::Destroy();
        return 0;
    }

} // namespace ns3

int main(int argc, char *argv[])
{
    return ns3::main(argc, argv);
}
