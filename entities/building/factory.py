from core.bases import BaseFactory
from .entity import Building


class Factory(BaseFactory):
    async def seed(self):
        fakes: list[Building] = [
            building for building in [
                Building(address = 'пр-т. Абая 157А, Алматы 050009', location = '!1m18!1m12!1m3!1d2906.5914716824514!2d76.88851371297018!3d43.23902427100445!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x38836916c79b7fa7%3A0xad3a9522a902a3b7!2z0JzQtdC00LjRhtC40L3RgdC60LjQuSDRhtC10L3RgtGAINCQ0LvQs9Cw0LzQtdC0IHwg0LDQvdCw0LvQuNC3INC90LAg0LrQvtGA0L7QvdCw0LLQuNGA0YPRgSwg0KPQl9CYLCDRgdC_0YDQsNCy0LrQuCDQkNC70LzQsNGC0Ys!5e0!3m2!1sru!2skz!4v1734653576619!5m2!1sru!2skz'),
                Building(address = 'ул. Малика Габдуллина 94/132, Алматы', location = '!1m18!1m12!1m3!1d22698.780176994962!2d76.89365334437086!3d43.23732113176!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x388368d806cfffff%3A0x1ad51b93ba5fc816!2z0JzQtdC00LjRhtC40L3RgdC60LjQuSDRhtC10L3RgtGAIE9uIENsaW5pYyDQkNC70LzQsNGC0YsgLSDQo9GA0L7Qu9C-0LMsINCf0YDQvtC60YLQvtC70L7Qsywg0JPQuNC90LXQutC-0LvQvtCz!5e0!3m2!1sru!2skz!4v1734653682695!5m2!1sru!2skz'),
                Building(address = '6WVH+5F2, ул. Кашгарская, Алматы 050000', location = '!1m18!1m12!1m3!1d22698.780176994962!2d76.89365334437086!3d43.23732113176!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x38836ecf11f57ddb%3A0xd4bb2e5dbded05a4!2z0JrQu9C40L3QuNC60LAg0JLQtdC6!5e0!3m2!1sru!2skz!4v1734653707962!5m2!1sru!2skz'),
                Building(address = 'пр-т. Абая 130, Алматы 050046', location = '!1m18!1m12!1m3!1d26892.756083610417!2d76.877599795627!3d43.230634438774615!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x388369ce4d0af171%3A0xf9d7d25fbb84eaab!2zTWFyaWEgQ2xpbmljLiDQkNCx0LDRjyAxMzA!5e0!3m2!1sru!2skz!4v1734653740839!5m2!1sru!2skz'),
                Building(address = 'улица Ауэзова 37, Алматы 050000', location = '!1m18!1m12!1m3!1d22657.211281647607!2d76.8826250573767!3d43.231693564609685!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3883694767aa91bb%3A0x38cdcc6ef0967999!2z0JzQtdC00LjRhtC40L3RgdC60LjQuSDQptC10L3RgtGAICLQkNCS0JXQodCi0JAi!5e0!3m2!1sru!2skz!4v1734653763707!5m2!1sru!2skz')
            ]
        ]
        await self.flush(fakes)
        return fakes