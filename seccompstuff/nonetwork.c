
#include <stdio.h>
#include <errno.h>

#include <unistd.h>

#include <sys/socket.h>
#include <sys/un.h>
#include <sys/prctl.h>

#include <seccomp.h>

int main(int argc, char** argv)
{
  prctl(PR_SET_NO_NEW_PRIVS, 1);
  // prctl(PR_SET_DUMPABLE, 0);

  scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);

#if defined(__i386__) || defined(__amd64__)
  seccomp_arch_add(ctx, SCMP_ARCH_X86);
  seccomp_arch_add(ctx, SCMP_ARCH_X86_64);
#endif

  int pf;
  for (pf = 0; pf != PF_MAX; ++pf) {
    if (pf == PF_LOCAL || pf == PF_NETLINK)
      continue;
    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(EACCES), SCMP_SYS(socket), 1,
      SCMP_CMP(0, SCMP_CMP_EQ, pf));
  }

  if (argc==1) {
    seccomp_export_pfc(ctx, 0);
    return 0;
  }

  seccomp_load(ctx);
  execvp(argv[1], argv+1);
  return 255;
}
