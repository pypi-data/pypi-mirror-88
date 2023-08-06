Inspired by quick.hook, this makes sending webhooks in discord .py much, much easier! 
Most of the functions below are wrapped in a:
```py
@bot.command
async def command(ctx):
```

#### IMPORTANT NOTE
for editors without pip, such as `repl.it`, to install the package, instead of `pip install ezhook` you would put the following at the top of your script:
```py
import os
os.system('pip install ezhook')
import ezhook
```


[Support Server](https://discord.gg/Av4KbrX)

# __**Examples:**__

## __**Without Embed:**__
```py
import ezhook
await ezhook.send_hook(
     bot = bot,
     channel = ctx.channel,
     message = "This is an example",
     username = "Space Boii",
     avatarURL = "https://i.imgur.com/EpTz5rOb.jpg",
)
```

![Without Embed](https://rjson.dev/ezhook/noembed.PNG)

_ _ _ _
_ _ _ _
_ _ _ _
_ _ _ _

## __**With Embed:**__
```py
import ezhook
embed=discord.Embed(title="example embed", color=3093151)
embed.add_field(name='hi',value="hello")
await ezhook.send_hook(
	bot = bot,
	channel = ctx.channel,
	message="This is an example",
	embed = embed,
	username = "Space Boii",
	avatarURL = "https://i.imgur.com/EpTz5rOb.jpg",
)
```
![With Embed](https://rjson.dev/ezhook/withembed.PNG)
_ _ _ _
_ _ _ _
