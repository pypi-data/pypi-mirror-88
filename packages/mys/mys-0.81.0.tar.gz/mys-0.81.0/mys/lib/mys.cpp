#include "mys.hpp"
#include "std/timer.hpp"
#include "std/thread.hpp"

List<String> create_args(int argc, const char *argv[])
{
    int i;
    List<String> args({});

    for (i = 0; i < argc; i++) {
        args.append(argv[i]);
    }

    return args;
}

std::ostream&
operator<<(std::ostream& os, const Exception& e)
{
    os << e.m_name_p << ": " << e.what();

    return os;
}

std::ostream&
operator<<(std::ostream& os, const std::exception& e)
{
    os << e.what();

    return os;
}

std::ostream&
operator<<(std::ostream& os, const String& obj)
{
    os << *obj.m_string;

    return os;
}

#if defined(MYS_TEST)

#define ANSI_COLOR_RED "\x1b[31m"
#define ANSI_COLOR_GREEN "\x1b[32m"
#define ANSI_COLOR_YELLOW "\x1b[33m"
#define ANSI_COLOR_BLUE "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN "\x1b[36m"

#define ANSI_BOLD "\x1b[1m"
#define ANSI_RESET "\x1b[0m"

#define COLOR(color, ...) ANSI_RESET ANSI_COLOR_##color __VA_ARGS__ ANSI_RESET

#define BOLD(...) ANSI_RESET ANSI_BOLD __VA_ARGS__ ANSI_RESET

#define COLOR_BOLD(color, ...)                                          \
    ANSI_RESET ANSI_COLOR_##color ANSI_BOLD __VA_ARGS__ ANSI_RESET

Test *tests_p = NULL;

#include <chrono>

using namespace std::chrono;

int main()
{
    Test *test_p;
    int passed = 0;
    int failed = 0;
    int total = 0;
    const char *result_p;

    test_p = tests_p;

    while (test_p != NULL) {
        auto begin = steady_clock::now();

        try {
            test_p->m_func();
            result_p = COLOR(GREEN, " ✔");
            passed++;
        } catch (std::exception &e) {
            std::cout << "Message: " << e << std::endl;
            result_p = COLOR(RED, " ✘");
            failed++;
        }

        auto end = steady_clock::now();
        auto duration = duration_cast<milliseconds>(end - begin).count();

        std::cout
            << result_p
            << " " << test_p->m_name_p
            << " (" <<  duration << " ms)"
            << std::endl;

        total++;
        test_p = test_p->m_next_p;
    }

    if (failed == 0) {
        return (0);
    } else {
        return (1);
    }
}

#elif defined(MYS_APPLICATION)

extern int package_main(int argc, const char *argv[]);

int main(int argc, const char *argv[])
{
    int res;

    try {
        res = package_main(argc, argv);
    } catch (std::exception &e) {
        std::cerr << e << std::endl;
        res = 1;
    }

    return (res);
}

#endif

namespace mys::thread
{

Stop::Stop(const char *reason)
{
}

Thread::Thread()
{
}

void Thread::start()
{
}

void Thread::stop()
{
}

void Thread::send_stop(std::shared_ptr<Stop> message)
{
}

void Thread::handle_stop(std::shared_ptr<Stop> message)
{
}

void Thread::join()
{
}

}

namespace mys::timer
{

Timer::Timer()
{
}

void Timer::start(float timeout)
{
}

void Timer::on_timeout()
{
}

}
