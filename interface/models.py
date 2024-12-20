from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=50)
    ocupied = models.BooleanField(default=False)
    perms = models.BooleanField(default=False) #Perms = 0 -> Sala inicial Perms = 1 -> 2nd Sala
    skin = models.ImageField(upload_to='skins/', default='skins/default_image.jpg')
    skin_hint = models.ImageField(upload_to='skins/', default='skins/default_image.jpg')
    skin_puzzle = models.ImageField(upload_to='skins/', default='skins/default_image.jpg')
    answer = models.CharField(max_length=50, default='')
    final = models.BooleanField(default=False)
    answers_to = models.ForeignKey('Room', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Character(models.Model):
    id = models.AutoField(primary_key=True)
    rule = models.CharField(max_length=50, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, default=None)   
    skin = models.ImageField(upload_to='skins/')
    avatar = models.ImageField(upload_to='skins/', default='skins/default_image.jpg')
    color = models.CharField(max_length=7, null=True, blank=True)
    last_room = models.BooleanField(default=False)

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    players = models.ManyToManyField('Player')

    def __str__(self):
        return self.name

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)
    discovered_rooms = models.ManyToManyField(Room, related_name='player', blank=True) 
    current_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_player')

    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    skin = models.ImageField(upload_to='skins/', default='skins/default.png')

    def __str__(self):
        return self.name

class Puzzle(models.Model):
    name = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    skin = models.ImageField(upload_to='skins/', default='skins/default.png')
    solution = models.CharField(max_length=50)

    def __str__(self):
        return self.name