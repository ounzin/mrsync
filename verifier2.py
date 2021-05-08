#!/usr/bin/env python3

import os, sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} com arg1 ... argn", file=sys.stderr)
        sys.exit(1)
    p = os.fork()
    if p == 0:  # Fils
        try:
            os.execvp(sys.argv[1], sys.argv[1:])
        except FileNotFoundError:
            print(f"Erreur lors du chargement de {sys.argv[1]}", file=sys.stderr)
            sys.exit(13)
    # Suite du père
    pid, status = os.wait()
    if os.WIFEXITED(status):
        code = os.WEXITSTATUS(status)
        if code == 0:
            print(f"Processus {p} terminé: succès")
        else:
            print(f"Processus {p} terminé : échec (code erreur: {code})")
    sys.exit(0)
