from model import Gen, Model

def start(initModel:list, countModel:int):
    initGens = [Gen(" ") for _ in range(len(initModel))]
    models = [Model(initGens, initModel) for _ in range(countModel)]
    return models

def run(initModel:list, countModel:int, prefModel:list[Model], run: bool):
    if len(prefModel) == 0:
        return start(initModel, countModel)
    else:
        if run:
            new_models:list[Model] = []
            for i in range(len(prefModel)):
                new_models.append(Model(prefModel[i].gens, initModel))
            
            return new_models