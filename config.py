CONFIG = {
	"screenName"         : ".50 BMG on my wing",
	"screenIcon"         : "./img/player.png",
	"screenSize"         : (480,640),
	"screenMargin"       : 50, #Object will killed if it is this much far (outside) from the border of the screen
	"FPS"                : 30,

	"playerSpeed"        : 2,
	"playerAmmo"         : [0,20], #Placeholder (unlimited MG), Bomb (INIT value)
	"playerAmmoRate"     : (50,1000), #Fire CD of each weapon in minisecond

	"enemyGenInterval"   : 0b11111,
	"enemyGenPosib"      : 50,
	"enemyHeavyMetal"    : 20,

	"displayAfterDmg"    : 50,

	"hitBonus"           : 5,
	"firingCost"         : 1,
	"hpAutoHeal"         : 100
}
