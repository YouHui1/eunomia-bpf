#ifndef _EXIT_SNOOP_BPF_H_
#define _EXIT_SNOOP_BPF_H_

#define TASK_COMM_LEN 16
#define MAX_FILENAME_LEN 127

struct event {
    int pid;
    int ppid;
    unsigned exit_code;
    unsigned long long duration_ns;
    char comm[TASK_COMM_LEN];
};

#endif // _EXIT_SNOOP_BPF_H_
