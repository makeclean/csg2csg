import subprocess


def cleanup():
    subprocess.check_call("rm -rf mcnp fluka openmc serpent file.mcnp", shell=True)


def test_windows_line_endings():

    subprocess.check_call(
        "csg2csg -i test-data/spheres.i -f mcnp -o all", shell=True
    )
    # UNIX to DOS  (adding CRs)
    subprocess.check_call(
        r"sed -e 's/$/\r/' test-data/spheres.i > spheres_win.i",
        shell=True,
    )
    subprocess.check_call(
        "csg2csg -i spheres_win.i -f mcnp -o all", shell=True
    )
    cleanup()


# round trip the MCNP file produced from the line above - it should be
# identical
def test_round_trip():
    cleanup()
    subprocess.check_call(
        "csg2csg -i test-data/spheres.i -f mcnp -o mcnp", shell=True
    )

    subprocess.check_call("mv mcnp/file.mcnp . ", shell=True)
    subprocess.check_call("rm -rf mcnp fluka openmc serpent", shell=True)

    subprocess.check_call(
        "csg2csg -i file.mcnp -f mcnp -o mcnp", shell=True
    )
    subprocess.check_call("diff file.mcnp mcnp/file.mcnp", shell=True)
    cleanup()
