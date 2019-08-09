import argparse
import json
import tempfile
from distutils.dir_util import copy_tree
from pathlib import Path

from azureml.core import Run, Workspace
from azureml.core.model import Model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model_name',
        type=str,
        default='',
        help='Name you want to give to the model.'
    )
    parser.add_argument(
        '--model_assets_path',
        type=str,
        nargs='+',
        default='outputs',
        help='Location(s) of trained model.'
    )

    args, unparsed = parser.parse_known_args()

    run = Run.get_context()
    ws = run.experiment.workspace

    tags = {
        "runId": str(run.id)
    }

    print(args.model_assets_path)
    print(json.dumps(tags))

    with tempfile.TemporaryDirectory() as tmpdir:
        merged_dir = os.path.join(tmpdir, "model")
        for model_dir in args.model_assets_path:
            copy_tree(model_dir, merged_dir)

        print("Registering model assets: {}".format(
            list(Path(tmpdir).iterdir())))
        model = Model.register(ws, model_name=args.model_name,
                               model_path=merged_dir, tags=tags)

        print('Model registered: {} \nModel Description: {} \nModel Version: {}'.format(
            model.name, model.description, model.version))
