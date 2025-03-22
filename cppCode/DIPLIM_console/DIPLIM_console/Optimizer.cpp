#include "Optimizer.h"

void Optimizer::initializeInfo()
{
    info["O"] = getOparams();
    info["F"] = getFparams();
    info["M"] = getMparams();

    double avg = field.avgerageField();
    if (!saveF) info["Details"] = nullptr;

    info["Time"] = std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>{
        {"Start", std::chrono::system_clock::now()},
        {"End", std::chrono::system_clock::now()},
        {"Total", std::chrono::system_clock::now()}
    };

    info["Base"] = std::map<std::string, double>{
        {"Start", field.calc_base()},
        {"End", 0},
        {"Diff", 0}
    };

    info["AVG"] = std::map<std::string, double>{
        {"Start", avg},
        {"End", 0},
        {"Diff", 0}
    };

    double max = field.maxField();
    info["MAX"] = std::map<std::string, double>{
        {"Start", max},
        {"End", 0},
        {"Diff", 0}
    };

    double min = field.minField();
    info["MIN"] = std::map<std::string, double>{
        {"Start", min},
        {"End", 0},
        {"Diff", 0}
    };

    info["Optimization"] = std::map<double, std::vector<Vector4D>>{};
    info["Optimization_Detailed"] = std::map<double, std::vector<Vector6D>>{};
}
