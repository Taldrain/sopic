from random import randint

from sopic.step import Step


class StoreData(Step):
    STEP_NAME = "store-data"

    def start(self, ctx, *kwargs):
        super().start()

        randomValue = randint(0, 9)
        # TODO use logger
        print(f'Storing random value: {randomValue}')

        ctx['foo'] = randomValue

        return self.OK()
