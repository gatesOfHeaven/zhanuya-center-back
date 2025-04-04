from random import choice

from core.bases import BaseFactory
from entities.user import User, Role
from entities.building import Building
from .entity import Manager


avatar_urls = [
    'https://hips.hearstapps.com/hmg-prod/images/portrait-of-a-happy-young-doctor-in-his-clinic-royalty-free-image-1661432441.jpg',
    'https://img.freepik.com/free-photo/beautiful-young-female-doctor-looking-camera-office_1301-7807.jpg?size=626&ext=jpg&ga=GA1.1.1819120589.1728345600&semt=ais_hybrid',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEfY2KLbSf8koPhOvfCUbMWFk8jCOL0MKn6w&s',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcST2DIwFY_oKUwagMh0Rx9B6Wy0k7xR0L-lvg&s',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSkN10j0GeME5_Ywkk9YYgW_ywwOjmmD7cZw&s',
    'https://snibbs.co/cdn/shop/articles/What_are_the_Challenges_of_Being_a_Doctor_1001x665.jpg?v=1684314843',
    'https://www.felixhospital.com/sites/default/files/2022-11/dr-ritesh-agarwal.jpg',
    'https://static.vecteezy.com/system/resources/thumbnails/028/287/555/small_2x/an-indian-young-female-doctor-isolated-on-green-ai-generated-photo.jpg',
    'https://media.istockphoto.com/id/179011088/photo/indian-doctor.jpg?s=612x612&w=0&k=20&c=EwRn1EWy79prCtdo8yHM6hvCVVcaKTznVBpVURPJxt4='
]


class Factory(BaseFactory):
    async def seed(self, users: list[User], buildings: list[Building]):
        fakes: list[Manager] = [Manager(
            profile = user,
            building = choice(buildings),
            avatar_url = choice(avatar_urls)
        ) for user in users if user.role_type == Role.MANAGER]
        
        await self.flush(fakes)
        return fakes