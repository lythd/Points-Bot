# Points-Bot
The Points Bot for Blue's Server, ready to Mine, Craft, Fight, Fish, Build Factories, Develop Plots, and More!

## To-Do List

### Plots
- Once you get some money its time to buy some plots to get some resources.
- You basically just wanna start by buying plots at certain locations. Each location has a few resources that it has, each of them with a min and max amount that will be in each plot bought. Locations also have other info like how windy it is or how sunny it is.
- Buying more than one plot in the same location just adds the new resources to the existing plot.
- Then you are able to collect a basic daily amount from those resources (depends on the resources, some might be 5 others 100, and not all resources can be collected, like oil has to be drilled), this amount represents what you harvest yourself, so its a small amount.
- You can check up on this every day and collect and sell the amounts.
- Unlike before there is no hourly resources, as whatever you buy is already there you just have to harvest it, the harvesting is done every day by you and every hour by your machines, since there is no buying of new plots there is no worry about buying at the wrong time and getting rid of some progress
- Plots get a lot faster once you can get some machines, machines can be bought from other people or made in factories. Machines drastically improve performance. Machines require power, a unit of energy (EU) is equal to 1 lampoil or 1 coal, and machines require a certain amount every hour, if the total machine power needed in a plot is not met then no machines will collect anything in that plot. Power must be generated on that plot (remember plots will be automatically merged). Wind and Solar are also options but depend on how windy and sunny it is in that location.
- You need some kind of Power Generator to generate power, these are the coal burner, oil burner, solar panel, and wind turbine. These are technically machines but have a very different purpose as they provide energy instead. Coal and oil burners will use the coal and lamp oil on the plot to make their power, they will only take 1 every hour so you will likely need quite a few. 1 coal/lampoil = 1 EU. Alternatively you can make a solar panel and wind turbine which don't require resources, these are a bigger investment as well as they are 5x more expensive to construct than their fossil fuel counterparts. They give power according to the sun and wind levels in that location, so are much better in some locations than others, but even if they are low they may be the only option if there is no coal or lampoil.
- plots command, /plots, Displays a list of how many plots you have in each location. Will also write something if that plot does not have enough energy so you can check for all plots at the same time.
- plot command, /plot <location>, Displays information of your plots in {location}, shows how many plots are in there, all the resources available, and the amount of machines in there, as well as energy produced and energy needed.
- plotbuy command, /plotbuy <location> {amount=1}, Buys {amount} plots in {location}.
- plotcollect command, /plotcollect, Collects your daily maximum from each plot, and collects your hourly bit from machines, these are kept track of seperately.
- plotconstruct command, /plotput <machine> <location> {amount=1}, Constructs {amount} of <machine> at <location>.
- plottransfer command, /plottake <machine> <fromlocation> <tolocation> {amount=1}, Moves {amount} of <machine> from <fromlocation> to <tolocation>. Use location of "storage" if you want to stop using something.
- plotmachines command, /plotmachines, Displays info about all the plotmachines.
- for plots, there would be some items the player can't harvest on their own, like oil needs to be drilled, emerald and ores need to be mined, and also i think for pumpkins making a pumpkin farm (which would technically be a machine) using pumpkin seeds would be the only way to get pumpkins. it also needs to give u seeds somehow, and it cant be crafting that defeats the whole point if u could craft a bunch from bought pumpkins (even if limiting to the pumpkin seed flag u can do that later and break), maybe like 1/5 pumpkins turn into a pumpkin seed, and farms require 20 seeds, that way it requires killing or buying quite a few to even getting started, and also limits growth if each one only has like 50/day. i like that, it is a weird exception for that to be the only additional item, but if theres more i can code it to take from file. the pumpkin farm would have the advantage of only requiring pumpkin seeds, no machines or anything, as well as pumpkins being very very abundant in the jungle, and giving a lot of pumpkins, maybe like double what other plots would give. the melon equivalent would be like automatic melon farm, and crafted using only one melon, but plenty of machines, so very expensive.
- plot accessories and stats and stuff, i think these would basically just multiply your daily manual resource collection limit, so with a diamond hoe, watering can, and a strawhat maybe you get +100% resource limit so you can collect double, also this would apply to all resources even if they don't fit the theme, though most of the manual ones are farming related anyway. this does not apply to the same resources for machine extraction.
- silicon extractor, machine for plots thats needed to get raw silicon

### Factories
- At last, the industrial revolution! Factories allow you to make complicated machines for plots and other factories, as well as certain items that are too complicated to craft, like metal bars from ores.
- There are a lot of factories and knowing what you need to make what can be complicated, so use /factorytiers to get a good view on progression. Factories on each tier can be made entirely from factories on the tier below. This isn't a strict rule though if you can get certain parts from someone else you can skip that.
- Once you have a good look and know what factory to start with, you can make that factory. Making works a lot like crafting however the result isn't an item its a factory, and you will always get one of a single type of a factory.
- After that you can use a factory to get items, keep in mind it may produce more than one item at a time so the total amount is not necessarily the same. Factories typically produce a single type of item but can produce more. Sometimes the factory name is the same as the item, but in other cases it might not be, so make sure you know.
- factorylist command, /factorylist, Displays a list of every factory type.
- factorytiers command, /factorytiers, Displays a list of every factory type in a tiered format to understand progression.
- factories command, /factories, Displays a list of all of your factories.
- factorymake command, /factorymake <factory> {amount=1}, Makes {amount} of <factory>.
- factoryuse command, /factoryuse <factory> {amount=1}, Uses a <factory> {amount> times.
- pumpkin pie factory that makes them for slightly cheaper
- various smelting/cooking factories, like for cooked cod/salmon and for glass, makes cheaper than any crafting if i do have a crafting
- caramel cloning facility, factory that duplicates caramels cream, i think caramel would start with the first caramels cream. the duplication would be pretty expensive, and the additional ingredient would probably be like a bunch of "raw materials" like 3 sand, 3 wood, 3 dirt, 3 stone.

### Quests
- Every day there is a new quest item that can only be obtained on that day. Check it out to see what location it is in, and whether you need to mine, fish, or fight to obtain it.
- Quests give you a sizeable reward and there is a quest leaderboard.
- You can collect multiple quest items in a day however you cannot trade or give them to any player, and only one can be submitted every day, so collecting more than one is useless.
- topquests command, /topquests {x=10}, Displays the top {x} people on the quest leaderboard.
- questview command, /questview, Views the daily quest item.
- questsubmit command, /questsubmit, Submits a daily quest item for a reward, can only be done once a day.

### Brewing
- brewing, not really required but id like to overhaul it, also this will pave the way for enchants, maybe make a copy of the old system incase i need to revert. brewing would be a stat, you need a witch hat in your armor slot, and a cauldron in your accessory slot. potion effects will be seperate from the old effects (which will now be called abilities) since they are scalable
- maybe some specific potion related accessories, like witches hat could buff your potions by 25%, and cauldron could debuff enemy potions by 25%. cauldron could also just have lots of defense since its made of a lot of iron (and a mana crystal, meaning the recipe only needs 1). the witches hat is a rare drop from witches. there would be upgrades but ill think abt those later, like maybe various runes which would replace cauldrons and give a bit better brewing stats, and also have a unique power. like a fire rune would damage your opponents with fire as like an additional effect (this and the wither effect would work opposite to how you might expect, in that you having the effect will damage your enemy). theres some other cool item possibilities, maybe an accessory that blocks effects from both sides.
- now the cool part, i think ill have a seperate bag from the main bag, maybe called the pouch, which can store items with data. the main ones being potions. this pouch would be capped at 15 items. you can sell these items to players with a special command called pouchoffer, which just works like offer but for this, the reason being is because you have to do special work since you can have multiple of a single item type and there would be no way to differentiate that for normal items, so in pouchoffer you give the pouch slot not the item name
- i think potions could just become a singular item now. when you brew a potion it will have a random strength for I to III, maybe there will be certain recipes to have multiple effects, but besides that you are stuck with one effect. this is based a lot on your brewing strength, so high brewing means you will get better strengths on average. for multi effect potions it gets harder, idk exactly how but for normal the base is I, and you roll between 0 and 2 to increase it more, with multi it'd b like I,I (or however many it is) and you roll between 0 and 2, 1 increases by 1, 2 increases by 1 and rolls again, by increase by 1 i mean it takes the lowest or the first if tied and increases.
- if you want to trash an item you can use /pouchsalvage, and that will give you a fixed cost for the item types, which is 50% market value if it has one, or a preset value for potions and anything else i think of (which is based on what their market value should be), or if i am missing anything then it defaults to 0 and gives a message saying to ask me since i forgot, and i will have to manually give them the money and set it. each brew gives you some experience, this is based on the total strength of what you brewed, so like II,I gets you 3 experience (meaning even if you don't need multi effect potions they will get you the most experiene). this works similarly to combat xp, and maybe it will be renamed that, and im not exactly sure how you will end up using it, but uh yeah. maybe certain mobs will drop like a fire rune template for instance, and you use xp to turn it into a normal fire rune. and there are tiers that require different levels of xp. maybe each rune also limits you to a certain list of potions you can craft. runes are immediate use for combat and for brewing.

### Enchantments
- enchantments, works similarly to brewing, but its a different system, needing wizard hats, and such. also just like potions its a one and done thing, so you cant double enchant your sword, you have to pick one enchant. all gear from enchants and brewing would be banned at first, and placed in my list of things to add, and added once i have an opening, since they can have cool effects like some i described above. ill do this after both though, since if i do brewing ill do enchantments, and there will be more items so yeah. scrolls instead of runes, and enchant xp not brewing xp. scroll restricts you to set enchants, maybe even directly. scrolls are used similarly.

### Elections
- elections, just preparing for them with some variables so i can easily apply some easy buffs. like lowered bcc for fishing, boosted doc for mining, boosts rarer enemies (just adds like 50 power to mob power), increased item chances (just adds like 25 power to fishing mining and fighting), sell percent (default is 10%), increased plot daily limit by 20%, 20% faster factories.
- there isnt much to code for elections, its just basically precoding a bunch of potential buffs by making them variables that can be changed when needed.

### Achievements
- achievements, these would be all the typical mob trophy items, but also the panzer, rocket, masterbolt, and other special items, as well as maybe the pumpkin farm, and some other notable things.

### Personal Statistics
- personal statistics, lets you see stuff like mobs killed, and all that stuff, general page then specific pages, have more statistics like for mining and fishing, pretty much each category in help would have a page for this

### Rewrite Help
- update/rewrite help, also split into two things, /help is for all commands, /guide is for important commands and for the text posts at the top (the current help). and maybe put together some posts for the forum
- make sure to review everything when rewriting help, something might have been missed that i previously mentioned as a feature, make sure everything there is working as intended, etc, not all of help i believe is accurate to what im doing anymore but still important to go through it all

### Wiki
- although there is the forum channel and help, i think a wiki is gonna go a long way, i was hesistant before but with all the locations with all the items you can get in each one, and all the mobs, it is going to be really tedious to use the bot to find the information, so i will make a wiki on fandom. and for when im doing the wiki remember zoglins are mini bosses, the wither is the only boss so far. also should clarify that a lot of stuff is not canon, for example fighting the wither is not part of the canon, nor is most item rewards like zombies dropping bars, and you mining netherite bars or titanium bars, though simpler items like finding fish and zombies are obviously canon. so ill clarify what is and isnt canon. also i can add estimated prices for all items, and these would be based on a basic value. like the comet fragments would be based on the 5% chance, and only using an old rod and the bait. this would be inclusive so includes the crafting items. this could also be done for those that are like crafted but also on market to give them a more accurate value. then id also have a paragraph explaining how i got this figure in case other people want to modify it or just know its true. also a page with achievements would be helpful, things for people to aim for besides money, and also a bit of an explanation on how to get them. 

### Gangs
- Gangs have been brought back! Gangs are a group of dedicated people trying to dominate the leaderboards together. We are still friendly to eachother, and there is nothing personal, but we have a friendly rivalry to see who can be on top.
- There are various things gangs can compete over, whether its places on money or items leaderboard, most total money, most total members, gang duel stats, and prestige. Prestige is my way of calculating a single metric based on everything else, however you may not value things the same way as mine so its not the be all and end all, and you shouldn't join a gang solely on its prestige, join one that will be the best for you.
- Gangs will have lots of gang exclusive stalls, likely selling items for cheap to help you out. Gangs also will have various specialties, for example a fishing gang, which has lots of fishing equipment they can sell you for cheap in their stalls, so if you are into fishing you would join them. The gang will likely say this in their description, as well as a list of achievements. Don't be afraid to give smaller less impressive gangs a shot too, they will probably give you more in benefits than the bigger ones!
- topmoney command, /topmoney {x=10}, Displays the top {x} people on the money leaderboard.
- topitem command, /topitem <item> {x=10}, Displays the top {x} people on the <item> leaderboard.
- topgangs command, /topgangs {x=10}, Displays the top {x} gangs on the gang prestige leaderboard.
- ganglist command, /ganglist, Displays a list of all gangs with descriptions and member counts.
- ganginfo command, /ganginfo <gang>, Displays info about a <gang>, including description, member count, total money, total quests, gang duel wins, gang duel losses, and prestige.
- gangjoin command, /gangjoin <gang>, Joins <gang>, leaves any gang you were in before.
- gangleave command, /gangleave, Leaves your gang.
- duel command, /duel <player> <money> {gang=False}, Sends a duel request to <player> for <money>, {gang} is whether it counts as a gang duel.
- duelaccept command, /duelaccept, Accepts a duel, and a fight occurs, make sure to equip before accepting.
- duelreject command, /duelreject, Rejects a duel.
- duelcancel command, /duelcancel, Cancels a duel.
- gangs is probably the last thing i will work on, i will probably make an annoucnement before just to get everyone ready and so people can start playing with the bot to get familiar, just to get it active, and also work a lot on the wiki. for gangs there will be join and leave, all the gang leaderboards, prioritise gang stalls, set stalls to gang only, etc, and for the shop 5% of the 10% that you don't receive goes to your gang, that doesn't make any difference, for stalls it will be smaller at only 1% since profit margins are tighter. also i need to ask whether nether star should be a godlike combat accessory, doing something like x1.5 every stat (which is really good but not undoubtedly the best so its still more fun, unlike netherite weapons which have to be powerful), or a drop accessory maybe like banning common drops or something strong. also remember to add the gang stats for duels.
- for duels have some banned items, these are permabanned for destroying the meta, some command to view these, starting out it will be all 3 netherite items, but flamethrower and rocket launcher might end up there, the reason they are banned not nerfed is that they make the meta stale, but still deserve to be good weapons for arena. however i think if i have weapon cycling it shouldnt matter, flamethrower just defeats any negative priority weapon cause its an insta kill already, let alone with a damage boost accessory, magic guard should help but still

### Wars
- Battles for wars is not planned to be implemented for the initial release, but I did already plan it out and include it in help since no one needs to know its not implemented yet (since there just are no battles)
- One of the main events its wars, although there are always border conflicts so you can fight, sometimes there will be an all out battle, and perhaps multiple if its a big war.
- A war does not necessarily mean there is a battle going on, I will likely have battles happening on weekends where more people can be active.
- The way a battle will work is they will have x amount of certain mobs, like 100 zombies and 40 skeletons, and we have to collectively beat all of them in a day. If a day passes and we do not beat them then we lose that battle and then lose that location, if we do beat all of them then we win the battle and win the location.
- Gaining and losing land has effects for all of us, so we all need to work together and help eachother.
- Fighting as normal on the location is seperate to battling and will still work as normal, so remember to battle and not fight.
- Also if you have tanks you can battle using those, each tank will kill a random number from 0 to 10 enemies
- battle command, /battle, Battles an enemy as part of the war, you need to be in the right location.
- tankbattle command, /tankbattle, Battles enemies using a tank as part of the war, you need to be in the right location.

### Combat Queue
**The combat queue is for items that I am thinking about adding but need an opening, either enough to add that it keeps a nice multiple (like 5 at a time) or a banned item in that category.**
- minibow, accessory, gives bow effect so allows you to shoot an arrow even if your holding a melee weapon, also would have to add some code to have tmp = count(Bow) + count(Rocket Launcher) + count(Star Launcher), and if tmp > 1: hits += tmp-1. that way the minibow will work even if you also have another bow, though if you have a rocket launcher neither will work since one won't have the ammo. fairly underpowered but i think its cool enough to add
- crossbow, weapon, not sure what makes it different from a regular bow, maybe a similar effect to sharp or something, and probably shoots bolts not arrows. so i guess its more 50:50 for piercing and blunt, and the sharp effect.
- lucky coin, accessory, already in but it could have some other effects relating to combat. critical chance, -10% acc, and just a general increase in drop items, like +20 power for those things.

### Misc Stuff
- temmie's pi crafting would only be available for temmie
- for the rocket trio, crafting unlocks after a rocket is produced
- commands for viewing all the info on items and mobs in different areas (try built into /mapinfo but that might be too much in one being 12 new fields) and info about mobs (/moblist + /mob <mob>).

## Future Update Ideas

### battles
- this would be needed for the war stuff
- cap of 50 so requires everyone to help, panzers still count as one each even tho u kill multiple

### crates
- automatic fishing item, wood iron gold and lava, lava is like a gold+ for only lava, these give some good items and a lot of ores, a lot of the weirder fishing drops would be moved into crates except biome specifics, and this will leave more room for cooler fishing related items, maybe even a jungle crate since there quite a few jungle items, this would be good for items like potions so you can get enough of them from a crate that its worth it to use potions
  
### kraken
- a special boss battle that you are able to summon using the suspicious eye. by special i mean unique, it will have its own command, and wont be something ill make more of, since well i want it to be special but also its specifically coded. it wont be like the other bosses, its stats will be in the function, and will have special attacks. also maybe a bit of lore, like it will say you embark on your boat, and the kraken might try to capsize you, reducing your damage, or something. idk i could do a lot with this.
  
### fishing up mobs
- either use fishing power as damage, or have them just also have damage, or maybe you have time to switch and you just do the command to fight it when you are ready, with a timelimit of like 5 minutes, or idk, have to talk abt it, this would be part of a great expansion update with lots of new items and such. this is a maybe im not really sure how i would do it, so might not happen.

### fighting
- maybe have like up to 3 weapons and u can choose which one at the start each turn, always ephemeral to not clog and to not show, idk but a fighting update is needed obv, more weapons and stuff too
