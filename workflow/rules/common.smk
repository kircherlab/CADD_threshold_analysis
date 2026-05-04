configfile: "config/config.yaml"


SCRIPTS_DIR = "../scripts"
ENVS_DIR = "../envs"


def getWorkflowFile(dir_name, name):
    return workflow.source_path("%s/%s" % (dir_name, name))


def getScript(name):
    return getWorkflowFile(SCRIPTS_DIR, name)


def getCondaEnv(name):
    return getWorkflowFile(ENVS_DIR, name)


def after_scoring_find_tsv_files():
    import glob
    return glob.glob(f"resources/scored/{config['name_scored']}*.tsv.gz")
