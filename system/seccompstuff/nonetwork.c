#include <stdio.h>
#include <stdlib.h>
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
  if (ctx == NULL)
    return 255;

#if defined(__i386__) || defined(__amd64__)
  uint32_t archs[] = { SCMP_ARCH_X86, SCMP_ARCH_X86_64, SCMP_ARCH_X32 };
#elif defined(__arm__) || defined(__arch64__)
  uint32_t archs[] = { SCMP_ARCH_ARCH, SCMP_ARCH_AARCH64 };
#elif defined(__mips__)
  uint32_t archs[] = { SCMP_ARCH_MIPS, SCMP_ARCH_MIPS64, SCMP_ARCH_MIPS64N32,
		       SCMP_ARCH_MIPSEL, SCMP_ARCH_MIPSEL64,
		       SCMP_ARCH_MIPEL64N32 };
#elif defined(__powerpc__) || defined(__powerpc64__)
  uint32_t archs[] = { SCMP_ARCH_PPC, SCMP_ARCH_PPC64, SCMP_ARCH_PPC64LE);
#else
  // We could use this:
  // uint32_t archs[] = { SCMP_ARCH_NATIVE };
  #error "I don't know about this target."
#endif

  for (unsigned i = 0; i < sizeof(archs) / sizeof(archs[0]); ++i) {
    int r = seccomp_arch_add(ctx, archs[i]);
    if (r < 0 && r != -EEXIST) {
      return 255;
    }
  }

  int pf;
  for (pf = 0; pf != PF_MAX; ++pf) {
    if (pf == PF_LOCAL || pf == PF_NETLINK)
      continue;
    int r = seccomp_rule_add(ctx, SCMP_ACT_ERRNO(EACCES), SCMP_SYS(socket), 1,
      SCMP_CMP(0, SCMP_CMP_EQ, pf));
    if (r < 0) {
      fprintf(stderr, "Could not add all seccomp BPF rule\n");
      return 255;
    }
  }

  if (argc == 1) {
    if (seccomp_export_pfc(ctx, 0) < 0) {
      fprintf(stderr, "Could not export seccomp BPF program\n");
      return 1;
    }
    return 0;
  }

  seccomp_load(ctx);
  execvp(argv[1], argv+1);
  return 255;
}
