# Data Registry

This registry tracks the datasets generated during the scraping and preprocessing phases.

| File / Directory Path | Phase         | Format            | Records | Status / Notes                                                            |
| :-------------------- | :------------ | :---------------- | :------ | :------------------------------------------------------------------------ |
| `data/raw/`           | Scraping      | Folder (JSON/MP4) | 9,504   | Scraped comments and metadata for all 67 target videos.                   |
| `data/processed/`     | Preprocessing | CSV               | 5,712   | Cleaned, language-filtered (EN/TL), and normalized comment dataset.       |
| `data/final/`         | Analysis      | CSV               | 5,712   | Final sentiment-scored dataset classified using multilingual XLM-RoBERTa. |

## Scraped Videos Log

This section lists the 67 scraped TikTok video IDs, authors, descriptions, comment counts, and dates.

| Video ID            | Author              | Description / Topic                                                             | Total Comments Scraped | Scraped Date |
| :------------------ | :------------------ | :------------------------------------------------------------------------------ | :--------------------- | :----------- |
| 7636796256186092820 | @unknown            | (Private/Unknown Video)                                                         | 118                    | 2026-06-30   |
| 7610204457997012238 | @_.\_kathy_.\_      | 🇵🇭 FILIPINOS & FILIPINO ALLIES!!! 🇵🇭 Check this on                              | 85                     | 2026-06-30   |
| 7596668243671059742 | @alta.co6           | Caseoh couldn’t believe how good this snack was #c                              | 303                    | 2026-06-30   |
| 7636050233251728671 | @appletree004       | That purple yam is the greatest thing in the world                              | 119                    | 2026-06-30   |
| 7568523925383105814 | @arawlondon         | Ube is everywhere these days - but why?⁠ ⁠ Let's s                              | 163                    | 2026-06-30   |
| 7490347763658607927 | @bitesofvancouver   | UBE ICE CREAM IS BACK AT SOFT PEAKS 🍠💜 UBE COCO PI                            | 206                    | 2026-06-30   |
| 7649421989114940692 | @bnc.ph             | PCCI: VIETNAM NEVER SATISFIED, CATCHING UP ON PH U                              | 200                    | 2026-06-30   |
| 7650435756334255381 | @bnc.ph             | PCCI: UBE COULD BE AT RISK OF BEING OVERSHADOWED B                              | 110                    | 2026-06-30   |
| 7519223374422281494 | @chariza\_          | Pret could never ✋! #ube #filipinodesserts 🇵🇭🍠🍵                              | 160                    | 2026-06-30   |
| 7505785307493764354 | @charmiejanee       | Filipino ube latte in the UK from Pret A Manger, l                              | 159                    | 2026-06-30   |
| 7624489818944277783 | @charmiejanee       | Trying to viral UBE latte drink in the Philippines                              | 116                    | 2026-06-30   |
| 7636758966596406551 | @charmiejanee       | My Filipino family and I tried the new Jollibee Ub                              | 63                     | 2026-06-30   |
| 7637043281548856590 | @cnn                | The purple yam is becoming a trendy ingredient in                               | 265                    | 2026-06-30   |
| 7626538022644862229 | @dom.skii           | chat is this a valid crashout #filipino #ube #phil                              | 191                    | 2026-06-30   |
| 7652206786878901525 | @dom.skii           | ube officer reporting for duty 🫡 honestly no hate                              | 150                    | 2026-06-30   |
| 7508569521192471838 | @eatsbynat          | Ube in three different forms, which Ube dessert is                              | 214                    | 2026-06-30   |
| 7360534922873900319 | @eatsbyrachel       | My comprehensive review of @Trader Joe's latest UB                              | 15                     | 2026-06-30   |
| 7522213513859796254 | @eatsbyrachel       | Why make ube mochi pancakes 🥞 or waffles 🧇 when yo                            | 0                      | 2026-06-30   |
| 7652304168119569682 | @erwan              | Everyday I see a new video uploaded about the popu                              | 166                    | 2026-06-30   |
| 7614371516238613767 | @eulahexplains      | Ube is a Filipino story 💜🇵🇭#education #funfacts #l                             | 132                    | 2026-06-30   |
| 7580174292575391006 | @fiberchina         | Purple Yams should be in everyone’s kitchen! #fyp                               | 52                     | 2026-06-30   |
| 7614663706043059487 | @foodfindsryan      | The largest Filipino food street fair is BACK 💜 Ub                             | 120                    | 2026-06-30   |
| 7611534322591354134 | @godsprincesss30    | as a half pinay abroad it makes so happy to see th                              | 86                     | 2026-06-30   |
| 7615453536687639821 | @hairbyjazie        | Learning moment for me. 💜 Ube is a purple yam that                             | 185                    | 2026-06-30   |
| 7640611415337815303 | @hopeindubai        | Me🤝ube #fyp #ube #filipinohusband #filipinofood #p                             | 50                     | 2026-06-30   |
| 7509991914230385951 | @iamliyahbiyah      | I WANNA BE A UBE CHEESECAKE OMG 🔥😍 #eating #ube #o                            | 0                      | 2026-06-30   |
| 7631972323679063304 | @iankewks           | Filipino Pantry Talk 3: Ube (Filipino Purple Yam).                              | 214                    | 2026-06-30   |
| 7638230639971470599 | @icechococake\_     | The ube taho from @Mang’s TAHO was one of the best                              | 111                    | 2026-06-30   |
| 7561324512495684876 | @iloveyochi         | Not your average root (vegetable) 😉 Oooooh babehhh                             | 187                    | 2026-06-30   |
| 7623742923674291478 | @isabelle199xxx     | What should I try next ? #philippines🇵🇭tiktok #ube                              | 141                    | 2026-06-30   |
| 7647215796443155745 | @itsbrovaski        | Filipino food keeps surprising me 🇵🇭🤯 Would you ea                             | 198                    | 2026-06-30   |
| 7417212304489467167 | @itscarterandalex   | Ube is uber delicious 🤤! You have to try when you                              | 161                    | 2026-06-30   |
| 7615205260272880927 | @jackiesanjose      | pronouncing “ube” as “oob” is honestly diobolical                               | 23                     | 2026-06-30   |
| 7473113232102739206 | @jaredsmall333      | Way better than Halo Halo lol #philippines🇵🇭tiktok                              | 40                     | 2026-06-30   |
| 7615481203948358914 | @jarofhibiscuss     | Ube EVERYTHING HALO HALO I CANT WAIT TO EAT YOUUUU                              | 146                    | 2026-06-30   |
| 7250017610648128810 | @jeanelleats        | 🥞 IF you want coconut syrup for your pancakes, do                              | 104                    | 2026-06-30   |
| 7626029757024537878 | @john.2_rosaros     | Pinoys 🇵🇭 try the viral Starbucks “UBE” #Ube #ubes                              | 125                    | 2026-06-30   |
| 7583459701552205076 | @joyceinloveandlife | Hawaii has many Filipinos so they have a great var                              | 273                    | 2026-06-30   |
| 7640099629484510484 | @justtonch          | Ube is Filipino. But the profits aren’t. The globa                              | 207                    | 2026-06-30   |
| 7616084559217675534 | @konstantinzsigo    | Would you try purple chocolate? Today, I’m announc                              | 334                    | 2026-06-30   |
| 7631745049180572941 | @kristinarodulfo    | I’m seeing ube EVERYWHERE from headlines in the NY                              | 137                    | 2026-06-30   |
| 7630047273770061077 | @kristypata         | Ube is so mashitda #ube #korean #filipino                                       | 50                     | 2026-06-30   |
| 7607630318534659349 | @kwamevlogs         | Trying UBE for the first time in Philippines #phil                              | 16                     | 2026-06-30   |
| 7629226105278336286 | @leilarfn           | ube ily, u deserve better 💜❤️‍🩹 #ube #filipinofood                               | 148                    | 2026-06-30   |
| 7619899577293917460 | @mau.wrob           | someone said more vlogs.. i guess this counts? 🤭 #                             | 177                    | 2026-06-30   |
| 7613917133264784653 | @melissaaltcakes    | My new favortie dessert🥔💗 #ube #cheesecake Ube Ha                             | 32                     | 2026-06-30   |
| 7508116696666803502 | @mukbangwithkay     | Trying Ube ONLY pastries in Orlando, Florida! ~ Wh                              | 263                    | 2026-06-30   |
| 7629680148282969364 | @news5everywhere    | Kung sobra-sobra ang supply ng mga gulay, ang ube                               | 199                    | 2026-06-30   |
| 7431583584768675118 | @njdotcom           | Ube is everywhere, but there’s something you need                               | 49                     | 2026-06-30   |
| 7647848903337053463 | @onefilipinotv      | 💜 Bonjour France! The Filipino Ube Craze Has Arriv                             | 81                     | 2026-06-30   |
| 7625306500772220190 | @pictureperfectluis | Everything I ate at UBELAND🤤🇵🇭 Vendors in the vid                              | 227                    | 2026-06-30   |
| 7649757461053820181 | @pohui_plus_pohui0  | Replying to @hi'ed my soul can rest now knowing I                               | 230                    | 2026-06-30   |
| 7353716817740778798 | @priceless          | 🟣🟣🟣 Where does ube come from? (Spoiler: the answer                           | 162                    | 2026-06-30   |
| 7376361109021871406 | @realandrecasper    | Filipino Ube Halaya. Buttery. Smooth. Sweet. 🍠🇵🇭#f                             | 158                    | 2026-06-30   |
| 7635620812334271765 | @russyap            | Lahat nalang iniimport natin pati ube                                           | 107                    | 2026-06-30   |
| 7643830807689170197 | @samkimarchives     | Koreans when they go to Philippine marts these day                              | 21                     | 2026-06-30   |
| 7641263536391458061 | @shaunsonexplains   | Most of the Ube products you’re tasting in the US                               | 214                    | 2026-06-30   |
| 7645758198380580110 | @shaunsonexplains   | Comment PURPLE if you want to learn the difference                              | 132                    | 2026-06-30   |
| 7561434566712642837 | @smollpol           | Like a girlie said in comments of that vid.. we’re                              | 193                    | 2026-06-30   |
| 7617153947555466509 | @spiceymac          | yall know im Filipino down #ube #ubetreats #filipi                              | 191                    | 2026-06-30   |
| 7619185307300285716 | @sugartokiee        | 말차코어 다음이라는 #우베코어 ?! 🍠 우베는 정말 제 취향이더랍니다 .. 💜 📍Yogur | 16                     | 2026-06-30   |
| 7616954054085774623 | @sweetlikehunnay    | The new iced ube coconut macchiato from Starbucks                               | 255                    | 2026-06-30   |
| 7616135959188393246 | @tautaifanok        | Try saying it to your Phillipino friend! #fyp #ube                              | 149                    | 2026-06-30   |
| 7629365696555830535 | @thefliphq          | Ube has officially conquered the world. What st                                 | 187                    | 2026-06-30   |
| 7617656811470048532 | @thereseabean       | If you really want to get to know the flavours of                               | 42                     | 2026-06-30   |
| 7492158527104912682 | @travelfuller       | Only eating ube for a whole day at Ube Land in New                              | 113                    | 2026-06-30   |
| 7614272794553093390 | @xtrememimi         | #stitch with @Jazie Deere im totally gonna start c                              | 263                    | 2026-06-30   |

## Search Methodology & Sampling Strategy

The dataset is selected using a **Keyword-Based Purposive Sampling** strategy targeting TikTok videos published between 2024 and 2026. A total of **67 videos** were curated for scraping.

### Sampling Criteria

1. **Search Keywords**: Videos were searched using the following query terms:
   - `ube`
   - `ube craze`
   - `trader joes ube`
   - `foreigner tries ube`
   - `purple yam`
   - `ube pronunciation`
2. **Engagement & Discussion Quality (Manual Verification)**:
   - **Like Verification**: Prioritized videos with relatively high like counts within each search query to ensure high reach and visibility.
   - **Discussion Scanning**: Scanned comment feeds to verify that the video generated active, meaningful, and relevant dialogue (such as discussions of cultural authenticity, heritage representation, or consumption behavior) rather than generic spam.
3. **Excluded Keywords**: Keywords like `filipino ube` and `ube taste test` were removed from active query lists as they did not yield distinct or significant additional search results.
