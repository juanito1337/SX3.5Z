import os, sys, json
sys.path.insert(0, os.path.join(os.getcwd(), 'projekt'))
import cnc_ansichtsmodell as model
with open(os.path.join(os.path.dirname(__file__), 'recipe_nx310.json'), 'x', encoding='utf8') as stream:
    json.dump(model.recipe(), stream, sort_keys=True, separators=(',', ':'))
print('NX_RECIPE_DUMP_OK ' + sys.version)
