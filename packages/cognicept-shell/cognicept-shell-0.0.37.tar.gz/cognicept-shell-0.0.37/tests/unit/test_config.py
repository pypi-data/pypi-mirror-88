
import pytest

from cogniceptshell.configuration import Configuration


def setup_file(tmpdir):
    p = tmpdir.join("runtime.env")
    p.write("COG_AGENT_CONTAINERS=container1;container2\nCOG_AGENT_IMAGES=image1;image2")


def test_yes_input():
    object = Configuration()
    assert (object.interpret_bool_input("Y") == True)

def test_no_input():
    object = Configuration()
    assert (object.interpret_bool_input("n") == False)

def test_other_input():
    object = Configuration()
    assert (object.interpret_bool_input("g") == None)
    assert (object.interpret_bool_input("%") == None)
    assert (object.interpret_bool_input("1") == None)
    assert (object.interpret_bool_input("akjflakjewr4f56f74ew@!!@$@!$") == None)

def test_is_ssh_disabled(tmpdir):
    setup_file(tmpdir)
    object = Configuration()
    object.load_config(str(tmpdir) + "/")
    assert (object.is_ssh_enabled() == False)    
    object.config["COG_ENABLE_SSH_KEY_AUTH"] = False
    assert (object.is_ssh_enabled() == False)

def test_is_ssh_disabled(tmpdir):
    setup_file(tmpdir)
    object = Configuration()
    object.load_config(str(tmpdir) + "/")
    object.config["COG_ENABLE_SSH_KEY_AUTH"] = True
    assert (object.is_ssh_enabled() == True)