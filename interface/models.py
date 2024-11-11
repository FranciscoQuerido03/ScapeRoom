from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=50)
    ocupied = models.BooleanField(default=False)
    perms = models.IntegerField(default=0)
    # skin = models.ImageField(upload_to='skins/', default='skins/default.png')


    def __str__(self):
        return self.name

class Character(models.Model):
    id = models.AutoField(primary_key=True)
    rule = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    skin = models.ImageField(upload_to='skins/', default='skins/default.png')

    def __str__(self):
        return self.name

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    players = models.ManyToManyField('Player')

    def __str__(self):
        return self.name

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)

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