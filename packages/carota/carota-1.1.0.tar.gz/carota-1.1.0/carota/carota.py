#!/bin/env/python

import argparse
import datetime
import random
import string
import uuid
import itertools

# Data
LASTNAME = ['Abbott','Acevedo','Acosta','Adams','Adkins','Aguilar','Aguirre','Alexander','Ali','Allen','Allison','Alvarado','Alvarez','Andersen','Anderson','Andrade','Andrews','Anthony','Archer','Arellano','Arias','Armstrong','Arnold','Arroyo','Ashley','Atkins','Atkinson','Austin','Avery','Avila','Ayala','Ayers','Bailey','Baird','Baker','Baldwin','Ball','Ballard','Banks','Barajas','Barber','Barker','Barnes','Barnett','Barr','Barrera','Barrett','Barron','Barry','Bartlett','Barton','Bass','Bates','Bauer','Bautista','Baxter','Bean','Beard','Beasley','Beck','Becker','Bell','Beltran','Bender','Benitez','Benjamin','Bennett','Benson','Bentley','Benton','Berg','Berger','Bernard','Berry','Best','Bird','Bishop','Black','Blackburn','Blackwell','Blair','Blake','Blanchard','Blankenship','Blevins','Bolton','Bond','Bonilla','Booker','Boone','Booth','Bowen','Bowers','Bowman','Boyd','Boyer','Boyle','Bradford','Bradley','Bradshaw','Brady','Branch','Brandt','Braun','Bray','Brennan','Brewer','Bridges','Briggs','Bright','Brock','Brooks','Brown','Browning','Bruce','Bryan','Bryant','Buchanan','Buck','Buckley','Bullock','Burch','Burgess','Burke','Burnett','Burns','Burton','Bush','Butler','Byrd','Cabrera','Cain','Calderon','Caldwell','Calhoun','Callahan','Camacho','Cameron','Campbell','Campos','Cannon','Cantrell','Cantu','Cardenas','Carey','Carlson','Carney','Carpenter','Carr','Carrillo','Carroll','Carson','Carter','Case','Casey','Castaneda','Castillo','Castro','Cervantes','Chambers','Chan','Chandler','Chaney','Chang','Chapman','Charles','Chase','Chavez','Chen','Cherry','Choi','Christensen','Christian','Chung','Church','Cisneros','Clark','Clarke','Clay','Clayton','Clements','Cline','Cobb','Cochran','Coffey','Cohen','Cole','Coleman','Collier','Collins','Colon','Combs','Compton','Conley','Conner','Conrad','Contreras','Conway','Cook','Cooke','Cooley','Cooper','Copeland','Cordova','Cortez','Costa','Cowan','Cox','Craig','Crane','Crawford','Crosby','Cross','Cruz','Cuevas','Cummings','Cunningham','Curry','Curtis','Dalton','Daniel','Daniels','Daugherty','Davenport','David','Davidson','Davies','Davila','Davis','Dawson','Day','Dean','Decker','Delacruz','Deleon','Delgado','Dennis','Diaz','Dickerson','Dickson','Dillon','Dixon','Dodson','Dominguez','Donaldson','Donovan','Dorsey','Dougherty','Douglas','Downs','Doyle','Drake','Duarte','Dudley','Duffy','Duke','Duncan','Dunlap','Dunn','Duran','Durham','Dyer','Eaton','Edwards','Elliott','Ellis','Ellison','English','Erickson','Escobar','Esparza','Espinoza','Estes','Estrada','Evans','Everett','Ewing','Farley','Farmer','Farrell','Faulkner','Ferguson','Fernandez','Ferrell','Fields','Figueroa','Finley','Fischer','Fisher','Fitzgerald','Fitzpatrick','Fleming','Fletcher','Flores','Flowers','Floyd','Flynn','Foley','Forbes','Ford','Foster','Fowler','Fox','Francis','Franco','Frank','Franklin','Frazier','Frederick','Freeman','French','Frey','Friedman','Fritz','Frost','Fry','Frye','Fuentes','Fuller','Gaines','Gallagher','Gallegos','Galloway','Galvan','Gamble','Garcia','Gardner','Garner','Garrett','Garrison','Garza','Gates','Gay','Gentry','George','Ghirardello','Gibbs','Gibson','Gilbert','Giles','Gill','Gillespie','Gilmore','Glass','Glenn','Glover','Golden','Gomez','Gonzales','Gonzalez','Good','Goodman','Goodwin','Gordon','Gould','Graham','Grant','Graves','Gray','Green','Greene','Greer','Gregory','Griffin','Griffith','Grimes','Gross','Guerra','Guerrero','Gutierrez','Guzman','Haas','Hahn','Hale','Haley','Hall','Hamilton','Hammond','Hampton','Hancock','Haney','Hanna','Hansen','Hanson','Hardin','Harding','Hardy','Harmon','Harper','Harrell','Harrington','Harris','Harrison','Hart','Hartman','Harvey','Hatfield','Hawkins','Hayden','Hayes','Haynes','Hays','Heath','Hebert','Henderson','Hendricks','Hendrix','Henry','Hensley','Henson','Herman','Hernandez','Herrera','Herring','Hess','Hester','Hickman','Hicks','Higgins','Hill','Hines','Hinton','Ho','Hobbs','Hodge','Hodges','Hoffman','Hogan','Holden','Holder','Holland','Holloway','Holmes','Holt','Hood','Hooper','Hoover','Hopkins','Horn','Horne','Horton','House','Houston','Howard','Howe','Howell','Huang','Hubbard','Huber','Hudson','Huerta','Huff','Huffman','Hughes','Hull','Humphrey','Hunt','Hunter','Hurley','Hurst','Hutchinson','Huynh','Ibarra','Ingram','Irwin','Jackson','Jacobs','Jacobson','James','Jarvis','Jefferson','Jenkins','Jennings','Jensen','Jimenez','Johns','Johnson','Johnston','Jones','Jordan','Joseph','Joyce','Juarez','Kaiser','Kane','Kaufman','Keith','Keller','Kelley','Kelly','Kemp','Kennedy','Kent','Kerr','Key','Khan','Kidd','Kim','King','Kirby','Kirk','Klein','Kline','Knapp','Knight','Knox','Koch','Kramer','Krause','Krueger','Lam','Lamb','Lambert','Landry','Lane','Lang','Lara','Larsen','Larson','Lawrence','Lawson','Le','Leach','Leblanc','Lee','Leon','Leonard','Lester','Levine','Levy','Lewis','Li','Lin','Lindsey','Little','Liu','Livingston','Lloyd','Logan','Long','Lopez','Love','Lowe','Lowery','Lozano','Lucas','Lucero','Luna','Lutz','Lynch','Lynn','Lyons','Macdonald','Macias','Mack','Madden','Maddox','Mahoney','Maldonado','Malone','Mann','Manning','Marks','Marquez','Marsh','Marshall','Martin','Martinez','Mason','Massey','Mata','Mathews','Mathis','Matthews','Maxwell','May','Mayer','Maynard','Mayo','Mays','Mcbride','Mccall','Mccann','Mccarthy','Mccarty','Mcclain','Mcclure','Mcconnell','Mccormick','Mccoy','Mccullough','Mcdaniel','Mcdonald','Mcdowell','Mcfarland','Mcgee','Mcgrath','Mcguire','Mcintosh','Mcintyre','Mckay','Mckee','Mckenzie','Mckinney','Mcknight','Mclaughlin','Mclean','Mcmahon','Mcmillan','Mcneil','Mcpherson','Meadows','Medina','Mejia','Melendez','Melton','Mendez','Mendoza','Mercado','Mercer','Merritt','Meyer','Meyers','Meza','Michael','Middleton','Miles','Miller','Mills','Miranda','Mitchell','Molina','Monroe','Montes','Montgomery','Montoya','Moody','Moon','Mooney','Moore','Mora','Morales','Moran','Moreno','Morgan','Morris','Morrison','Morrow','Morse','Morton','Moses','Mosley','Moss','Moyer','Mueller','Mullen','Mullins','Munoz','Murillo','Murphy','Murray','Myers','Nash','Navarro','Neal','Nelson','Newman','Newton','Nguyen','Nichols','Nicholson','Nielsen','Nixon','Noble','Nolan','Norman','Norris','Norton','Novak','Nunez','Obrien','Ochoa','Oconnell','Oconnor','Odom','Odonnell','Oliver','Olsen','Olson','Oneal','Oneill','Orozco','Orr','Ortega','Ortiz','Osborn','Osborne','Owen','Owens','Pace','Pacheco','Padilla','Page','Palmer','Park','Parker','Parks','Parrish','Parsons','Patel','Patrick','Patterson','Patton','Paul','Payne','Pearson','Peck','Pena','Pennington','Perez','Perkins','Perry','Peters','Petersen','Peterson','Petty','Pham','Phelps','Phillips','Pierce','Pineda','Pittman','Pitts','Pollard','Ponce','Poole','Pope','Porter','Potter','Potts','Powell','Powers','Pratt','Preston','Price','Prince','Proctor','Pruitt','Pugh','Quinn','Ramirez','Ramos','Ramsey','Randall','Randolph','Rangel','Rasmussen','Ray','Raymond','Reed','Reese','Reeves','Reid','Reilly','Reyes','Reynolds','Rhodes','Rice','Rich','Richard','Richards','Richardson','Richmond','Riddle','Riggs','Riley','Rios','Ritter','Rivas','Rivera','Rivers','Roach','Robbins','Roberson','Roberts','Robertson','Robinson','Robles','Rocha','Rodgers','Rodriguez','Rogers','Rojas','Rollins','Roman','Romero','Rosales','Rosario','Rose','Ross','Roth','Rowe','Rowland','Roy','Rubio','Ruiz','Rush','Russell','Russo','Ryan','Salas','Salazar','Salinas','Sampson','Sanchez','Sanders','Sandoval','Sanford','Santana','Santiago','Santos','Saunders','Savage','Sawyer','Schaefer','Schmidt','Schmitt','Schneider','Schroeder','Schultz','Schwartz','Scott','Sellers','Serrano','Sexton','Shaffer','Shah','Shannon','Sharp','Shaw','Shea','Shelton','Shepard','Shepherd','Sheppard','Sherman','Shields','Short','Silva','Simmons','Simon','Simpson','Sims','Singh','Singleton','Skinner','Sloan','Small','Smith','Snow','Snyder','Solis','Solomon','Sosa','Soto','Sparks','Spears','Spence','Spencer','Stafford','Stanley','Stanton','Stark','Steele','Stein','Stephens','Stephenson','Stevens','Stevenson','Stewart','Stokes','Stone','Stout','Strickland','Strong','Stuart','Suarez','Sullivan','Summers','Sutton','Swanson','Sweeney','Tanner','Tapia','Tate','Taylor','Terrell','Terry','Thomas','Thompson','Thornton','Todd','Torres','Townsend','Tran','Travis','Trevino','Trujillo','Tucker','Turner','Tyler','Underwood','Valdez','Valencia','Valentine','Valenzuela','Vance','Vang','Vargas','Vasquez','Vaughan','Vaughn','Vazquez','Vega','Velasquez','Velazquez','Velez','Villa','Villanueva','Villarreal','Villegas','Vincent','Wade','Wagner','Walker','Wall','Wallace','Waller','Walls','Walsh','Walter','Walters','Walton','Wang','Ward','Ware','Warner','Warren','Washington','Waters','Watkins','Watson','Watts','Weaver','Webb','Weber','Webster','Weeks','Weiss','Welch','Wells','Werner','West','Wheeler','Whitaker','White','Whitehead','Whitney','Wiggins','Wilcox','Wiley','Wilkerson','Wilkins','Wilkinson','Williams','Williamson','Willis','Wilson','Winters','Wise','Wolf','Wolfe','Wong','Wood','Woodard','Woods','Woodward','Wright','Wu','Wyatt','Yang','Yates','Yoder','York','Young','Yu','Zamora','Zavala','Zhang','Zimmerman','Zuniga']
FEMALE_NAMES = ['Abbie','Ada','Adaline','Addie','Adela','Adelaide','Adele','Adelia','Adelina','Adeline','Adell','Adella','Adelle','Adrienne','Agatha','Agnes','Aida','Aileen','Alba','Alberta','Albertha','Albina','Alda','Alene','Aletha','Alfreda','Alice','Alicia','Aline','Allene','Allie','Alma','Almeda','Almeta','Alpha','Alta','Altha','Althea','Alva','Alvera','Alverta','Alvina','Alyce','Amalia','Amanda','Amelia','Amie','Amy','Ana','Anastasia','Andrea','Angela','Angelina','Angeline','Angelita','Angie','Anita','Ann','Anna','Annabel','Annabell','Annabelle','Annamae','Anne','Annetta','Annette','Annie','Antionette','Antoinette','Antonette','Antonia','Ardell','Ardella','Ardis','Ardith','Arleen','Arlene','Arlie','Arline','Artie','Arvilla','Audie','Audra','Audrey','Audry','Augusta','Augustine','Aurelia','Aurora','Ava','Avis','Barbara','Beatrice','Beaulah','Bella','Belle','Belva','Bennie','Bernadette','Bernadine','Bernardine','Berneice','Bernice','Berniece','Bernita','Berta','Bertha','Bertie','Beryl','Bess','Bessie','Beth','Bethel','Betsy','Bette','Bettie','Betty','Bettye','Beulah','Beverley','Beverly','Billie','Billy','Billye','Birdie','Birtha','Blanch','Blanche','Blossom','Bobbie','Bobby','Bonita','Bonnie','Bridget','Bulah','Burnice','Callie','Camilla','Camille','Carlene','Carmel','Carmela','Carmelita','Carmella','Carmen','Carol','Carole','Carolina','Caroline','Carolyn','Carrie','Cassie','Catalina','Catharine','Catherine','Cathleen','Cathrine','Cathryn','Cecelia','Cecil','Cecile','Cecilia','Celeste','Celestine','Celia','Ceola','Charity','Charlene','Charles','Charlie','Charline','Charlotte','Chloe','Christeen','Christene','Christina','Christine','Claire','Clara','Clare','Clarice','Clarissa','Claudia','Claudie','Claudine','Clementine','Cleo','Cleta','Clyde','Colleen','Concepcion','Concetta','Concha','Connie','Constance','Consuelo','Cora','Coral','Cordelia','Corene','Corine','Corinne','Cornelia','Corrie','Corrine','Crystal','Cynthia','Daisy','Dale','Dana','Daphne','Darleen','Darlene','Darline','Dawn','Deborah','Delfina','Delia','Delilah','Della','Delma','Delores','Deloris','Delpha','Delphia','Delphine','Delta','Dena','Dessie','Diana','Diane','Dimple','Dixie','Dollie','Dolly','Dolores','Dominga','Dona','Donald','Donna','Donnie','Dora','Dorathy','Dorcas','Doreen','Doretha','Doris','Dorotha','Dorothea','Dorothy','Dorris','Dortha','Dorthy','Dottie','Dovie','Drucilla','Earlene','Earline','Earnestine','Easter','Eda','Eddie','Edith','Edna','Edward','Edwina','Edyth','Edythe','Effie','Eileen','Elaine','Elayne','Elda','Eldora','Eleanor','Eleanora','Eleanore','Elease','Elena','Elenor','Elenora','Elinor','Elinore','Elisa','Elisabeth','Elise','Eliza','Elizabeth','Elizebeth','Ella','Ellamae','Ellen','Ellie','Elma','Elmira','Elna','Elnora','Eloisa','Eloise','Elouise','Elsa','Elsie','Elva','Elvera','Elvie','Elvina','Elvira','Elwanda','Emilia','Emilie','Emily','Emma','Emmie','Emogene','Enid','Enola','Era','Erline','Erma','Erna','Ernestine','Esperanza','Essie','Esta','Estell','Estella','Estelle','Ester','Esther','Ethel','Ethelene','Ethelyn','Etta','Eudora','Eugenia','Eula','Eulah','Eulalia','Euna','Eunice','Eva','Evalyn','Evangeline','Eve','Eveline','Evelyn','Evelyne','Evie','Fairy','Faith','Fannie','Fanny','Fay','Faye','Felicia','Fern','Ferne','Filomena','Flora','Florence','Florene','Florida','Florine','Flossie','Floy','Frances','Francine','Francis','Francisca','Frank','Frankie','Freda','Freddie','Freeda','Freida','Frieda','Gail','Garnet','Garnett','Gayle','Gaynell','Gearldine','Gene','Geneva','Genevieve','George','Georgene','Georgette','Georgia','Georgiana','Georgianna','Georgie','Georgina','Geraldine','Germaine','Gerry','Gertie','Gertrude','Gilda','Gladys','Glenda','Glenna','Gloria','Golda','Goldia','Goldie','Grace','Gracie','Grayce','Greta','Gretchen','Guadalupe','Gussie','Gwen','Gwendolyn','Hallie','Hannah','Harold','Harriet','Harriett','Harriette','Hattie','Hazel','Hazle','Hedwig','Helen','Helena','Helene','Hellen','Henrietta','Henry','Hester','Hettie','Hilda','Hildegarde','Hildred','Hilma','Hope','Hortencia','Hortense','Hulda','Ida','Idell','Idella','Ila','Ilene','Ima','Imogene','Ina','Ines','Inez','Iola','Iona','Ione','Ira','Irene','Irine','Iris','Irma','Isabel','Isabell','Isabella','Isabelle','Iva','Ivory','Ivy','Jack','Jackie','Jacqueline','Jacquelyn','James','Jamie','Jane','Janet','Janette','Janice','Janie','Janis','Jannie','Jaunita','Jayne','Jean','Jeane','Jeanette','Jeanne','Jeannette','Jennie','Jenny','Jerry','Jessie','Jettie','Jewel','Jewell','Jimmie','Jo','Joan','Joann','Joanna','Joanne','Joe','Johanna','John','Johnie','Johnnie','Jonnie','Josefa','Josefina','Joseph','Josephine','Josie','Joy','Joyce','Juana','Juanita','Judith','Judy','Julia','Juliana','Julie','Juliet','Juliette','June','Justine','Kate','Katharine','Katherine','Katheryn','Kathleen','Kathlyn','Kathrine','Kathryn','Kathryne','Katie','Kattie','Kay','Kitty','Larue','Laura','Laurel','Lauretta','Laurette','Laurine','Lavada','Lavera','Lavern','Laverna','Laverne','Lavina','Lavinia','Lavon','Lavonne','Lea','Leah','Leatha','Leatrice','Lee','Leila','Lela','Lelia','Lena','Lennie','Lenora','Lenore','Leola','Leona','Leone','Leonor','Leonora','Leonore','Leora','Leota','Leslie','Lessie','Leta','Letha','Letitia','Lettie','Libby','Lida','Lila','Lilia','Lilian','Lilla','Lillian','Lillie','Lilly','Lily','Lina','Linda','Linnie','Lizzie','Lois','Lola','Lona','Lonnie','Lora','Loraine','Lorayne','Lorena','Lorene','Loretta','Lorine','Lorna','Lorraine','Lottie','Lou','Louella','Louis','Louisa','Louise','Lovie','Loyce','Lucia','Lucie','Lucile','Lucille','Lucinda','Lucretia','Lucy','Ludie','Lue','Luella','Luisa','Lula','Lulu','Lupe','Lura','Lurline','Luvenia','Luz','Lyda','Lydia','Lyla','Lynn','Mabel','Mable','Macie','Madaline','Madalyn','Madeleine','Madeline','Madelyn','Madge','Madie','Madlyn','Madonna','Mae','Mafalda','Magdalen','Magdalena','Magdalene','Maggie','Magnolia','Malinda','Mallie','Mamie','Mammie','Mandy','Manuela','Marcella','Marcelle','Marcia','Margaret','Margarete','Margarett','Margaretta','Margarette','Margarita','Marge','Margery','Margie','Margret','Marguerite','Margurite','Maria','Marian','Marianna','Marianne','Marie','Marietta','Marilyn','Marilynn','Marion','Marjorie','Marjory','Marlene','Martha','Martina','Marvel','Mary','Maryann','Marybelle','Maryellen','Maryjane','Marylou','Marylouise','Mathilda','Matilda','Mattie','Maud','Maude','Maudie','Maureen','Maurice','Maurine','Mavis','Maxie','Maxine','May','Maybell','Maybelle','Mayme','Mazie','Melba','Melissa','Melva','Melvina','Mercedes','Meredith','Merle','Meta','Mickey','Mildred','Millicent','Millie','Mina','Minerva','Minnie','Miriam','Mittie','Mollie','Molly','Mona','Monica','Mozell','Mozelle','Muriel','Myra','Myrl','Myrle','Myrna','Myrtice','Myrtie','Myrtis','Myrtle','Nadine','Nan','Nancy','Nannie','Naoma','Naomi','Natalie','Nathalie','Nedra','Nelda','Nell','Nella','Nelle','Nellie','Neoma','Neta','Nettie','Neva','Nila','Nina','Nita','Nola','Nona','Nora','Noreen','Norene','Norine','Norma','Nova','Novella','Ocie','Octavia','Odell','Odessa','Ofelia','Ola','Olene','Oleta','Olga','Olive','Olivia','Ollie','Oma','Ona','Oneida','Oneta','Opal','Ophelia','Ora','Orpha','Ossie','Ouida','Palma','Pansy','Pat','Patricia','Patsy','Pattie','Patty','Paul','Paula','Pauline','Pearl','Pearle','Pearlie','Pearline','Peggy','Penelope','Petra','Philomena','Phoebe','Phyllis','Pinkie','Polly','Priscilla','Prudence','Queen','Queenie','Rachael','Rachel','Rae','Ramona','Ray','Reba','Rebecca','Regina','Rena','Renee','Reta','Retha','Retta','Reva','Rhea','Rhoda','Richard','Rita','Robbie','Robert','Roberta','Roma','Romaine','Rosa','Rosalee','Rosalia','Rosalie','Rosalind','Rosaline','Rosalyn','Rosamond','Rosanna','Rose','Rosella','Roselyn','Rosemarie','Rosemary','Rosetta','Rosia','Rosie','Rosina','Roslyn','Rowena','Roxie','Roy','Rozella','Rubie','Ruby','Rubye','Ruth','Ruthe','Ruthie','Sabina','Sadie','Sallie','Sally','Sammie','Sandra','Santa','Santina','Santos','Sara','Sarah','Savannah','Selma','Sheila','Shirlee','Shirley','Sibyl','Socorro','Sofia','Sonia','Sophia','Sophie','Stasia','Stella','Stephanie','Sudie','Sue','Susan','Susanna','Susanne','Susie','Suzanne','Sybil','Syble','Sylvia','Tennie','Teresa','Terry','Tessie','Theda','Thelma','Theo','Theodora','Theresa','Therese','Thomas','Tillie','Tina','Tomasa','Tommie','Tressie','Treva','Trinidad','Twila','Una','Ursula','Vada','Valeria','Valerie','Veda','Velda','Velma','Velva','Vena','Venita','Vera','Verda','Verdie','Vergie','Verla','Verlie','Verna','Vernell','Vernice','Vernie','Vernon','Verona','Veronica','Versie','Vesta','Veva','Victoria','Vida','Vina','Vincenza','Viola','Violet','Violette','Virgie','Virginia','Vita','Viva','Vivian','Vivien','Vivienne','Walter','Wanda','Waneta','Wilda','Wilhelmina','Willa','Willene','Willia','William','Willie','Wilma','Winifred','Winnie','Winnifred','Winona','Wynona','Yetta','Yolanda','Yoshiko','Yvette','Yvonne','Zelda','Zella','Zelma','Zita','Zoe','Zola','Zona','Zora','Zula']
MALE_NAMES = ['Aaron','Abe','Abel','Abner','Abraham','Abram','Adam','Addison','Adelbert','Adolfo','Adolph','Adolphus','Adrian','Al','Alan','Albert','Alberto','Albin','Alden','Aldo','Alec','Alejandro','Alex','Alexander','Alfonso','Alford','Alfred','Alfredo','Allan','Allen','Allie','Allison','Alois','Alonzo','Aloysius','Alphonse','Alphonso','Alton','Alva','Alvie','Alvin','Alvis','Ambrose','Americo','Amos','Anderson','Andres','Andrew','Andy','Angel','Angelo','Angus','Anthony','Anton','Antone','Antonio','Archibald','Archie','Arden','Arley','Arlie','Arlo','Armand','Armando','Armond','Arnold','Aron','Art','Arther','Arthur','Artie','Artis','Arturo','Arvel','Arvid','Arvil','Arvin','Asa','Ashley','Aubrey','Audrey','August','Augustine','Augustus','Austin','Author','Avery','Barney','Barton','Basil','Ben','Benedict','Benito','Benjamin','Benjiman','Bennett','Bennie','Benny','Benton','Bernard','Bernice','Bernie','Berry','Bert','Bertram','Bertrand','Beryl','Beverly','Bill','Billie','Billy','Blaine','Blair','Bob','Bobbie','Bobby','Bonnie','Booker','Boyce','Boyd','Bradford','Bradley','Brady','Brice','Brooks','Brown','Bruce','Bruno','Bryan','Bryant','Bryce','Buck','Bud','Buddy','Buel','Buford','Burdette','Burl','Burley','Burnell','Burt','Burton','Buster','Byron','Caesar','Caleb','Calvin','Cameron','Carey','Carl','Carleton','Carlo','Carlos','Carlton','Carlyle','Carmelo','Carmen','Carmine','Carol','Carrol','Carroll','Carson','Carter','Cary','Casimer','Casimir','Casper','Cecil','Charles','Charley','Charlie','Chauncey','Chester','Chris','Christ','Christian','Christopher','Clair','Claire','Clarance','Clare','Clarence','Clark','Claud','Claude','Claudie','Clay','Clayton','Clem','Clemens','Clement','Cleo','Cleon','Cletus','Cleve','Cleveland','Clifford','Clifton','Clint','Clinton','Clovis','Cloyd','Clyde','Coleman','Columbus','Connie','Conrad','Constantine','Cornelius','Coy','Craig','Crawford','Cruz','Curtis','Cyril','Cyrus','Dale','Dallas','Dalton','Damon','Dan','Dana','Daniel','Danny','Dante','Darrel','Darrell','Darwin','Daryl','Dave','David','Davis','Dayton','Dean','Dee','Delbert','Delmar','Delmer','Delton','Dempsey','Denis','Dennis','Denver','Denzil','Desmond','Dewayne','Dewey','Dewitt','Dexter','Dick','Dillard','Dock','Domenic','Domenick','Domingo','Dominic','Dominick','Don','Donal','Donald','Donnie','Donovan','Doris','Dorothy','Dorris','Dorsey','Douglas','Doyle','Duane','Dudley','Duncan','Durward','Durwood','Dwayne','Dwight','Earl','Earle','Earlie','Early','Earnest','Ed','Edd','Eddie','Edgar','Edison','Edmond','Edmund','Edsel','Eduardo','Edward','Edwin','Elbert','Elden','Eldon','Eldred','Eldridge','Elgin','Eli','Elias','Elijah','Elisha','Elliot','Elliott','Ellis','Ellsworth','Ellwood','Elmer','Elmo','Elmore','Eloy','Elroy','Elton','Elvin','Elvis','Elwin','Elwood','Elwyn','Elza','Elzie','Emanuel','Emerson','Emery','Emil','Emile','Emilio','Emmet','Emmett','Emmit','Emmitt','Emory','Ennis','Enoch','Enrico','Enrique','Eric','Ernest','Ernesto','Ernie','Ervin','Erwin','Estel','Eugene','Evan','Evans','Everett','Everette','Evert','Ewell','Ezekiel','Ezell','Ezra','Fay','Felipe','Felix','Felton','Ferdinand','Fernand','Fernando','Ferris','Fidel','Finis','Fletcher','Florian','Floyd','Ford','Forest','Forrest','Foster','Foy','Frances','Francis','Francisco','Frank','Frankie','Franklin','Franklyn','Fred','Freddie','Frederic','Frederick','Fredric','Fredrick','Freeman','Fritz','Furman','Gabriel','Gaetano','Gail','Gale','Galen','Gardner','Garfield','Garland','Garnett','Garrett','Garth','Gary','Gaston','Gayle','Gaylord','Gene','General','George','Gerald','Gerard','Gilbert','Gilberto','Giles','Gino','Glen','Glendon','Glenn','Gorden','Gordon','Grady','Graham','Grant','Granville','Gregorio','Gregory','Grover','Guadalupe','Guido','Guillermo','Gus','Gustav','Gustave','Guy','Hal','Hamilton','Hampton','Hans','Harding','Hardy','Harlan','Harland','Harlen','Harley','Harmon','Harold','Harris','Harrison','Harry','Harvey','Harvie','Haskell','Hayden','Hayward','Haywood','Hazel','Hector','Helen','Henderson','Henery','Henry','Herbert','Herman','Hermon','Herschel','Hershel','Hilbert','Hillard','Hilton','Hiram','Hiroshi','Hobart','Hobert','Hollis','Homer','Horace','Houston','Howard','Howell','Hoyt','Hubert','Huey','Hugh','Hugo','Hunter','Huston','Hyman','Ignacio','Ignatius','Ike','Ira','Irvin','Irving','Irwin','Isaac','Isadore','Isaiah','Isiah','Isidore','Israel','Issac','Ivan','Ivory','Ivy','Jack','Jackie','Jackson','Jacob','Jake','James','Jarvis','Jason','Jasper','Jay','Jean','Jeff','Jefferson','Jennings','Jerald','Jeremiah','Jerome','Jerry','Jess','Jesse','Jessie','Jesus','Jewel','Jewell','Jim','Jimmie','Jimmy','Joaquin','Joe','Joel','Joesph','John','Johnie','Johnnie','Johnny','Johnson','Jon','Jonas','Jonathan','Jonnie','Jordan','Jose','Joseph','Joshua','Joy','Juan','Judge','Judson','Jules','Julian','Julio','Julius','June','Junior','Junius','Justin','Karl','Kay','Kazuo','Keith','Kelly','Kendall','Kenneth','Kent','Kermit','Kevin','King','Kirby','Kiyoshi','Kyle','Lacy','Lafayette','Lamar','Lambert','Larry','Laurel','Lauren','Laurence','Lavern','Laverne','Lawerence','Lawrence','Lawson','Leamon','Leander','Lee','Leeroy','Leland','Lemuel','Lenard','Leo','Leon','Leonard','Leopold','Leroy','Lesley','Leslie','Lester','Levi','Levy','Lewis','Lincoln','Lindsey','Linwood','Lionel','Llewellyn','Lloyd','Logan','Lois','Lon','Lonnie','Lonzo','Loran','Loren','Lorenzo','Lorin','Louie','Louis','Lowell','Loy','Loyal','Loyd','Luca','Lucian','Lucien','Lucious','Lucius','Ludwig','Luis','Luke','Lupe','Luther','Lyle','Lyman','Lynn','Mac','Mack','Madison','Mahlon','Major','Malcolm','Malvin','Manley','Manuel','Marcel','Marcellus','Marco','Marcus','Margarito','Mariano','Mario','Marion','Mark','Marlin','Marshal','Marshall','Martin','Marvin','Mary','Masao','Mason','Mathew','Matt','Matteo','Matthew','Maurice','Max','Maxie','Maxwell','Maynard','Mckinley','Melton','Melville','Melvin','Meredith','Merl','Merle','Merlin','Merlyn','Merrill','Merritt','Merton','Mervin','Merwin','Meyer','Michael','Micheal','Mickey','Miguel','Mike','Milan','Milburn','Miles','Milford','Millard','Miller','Milo','Milton','Mitchel','Mitchell','Monroe','Morgan','Morris','Mortimer','Morton','Mose','Moses','Murl','Murphy','Murray','Murry','Myles','Myron','Napoleon','Nathan','Nathaniel','Neal','Ned','Neil','Nelson','Newell','Newton','Nicholas','Nick','Nickolas','Nicolas','Noah','Noble','Noel','Nolan','Norbert','Norman','Normand','Norris','Norval','Norwood','Nunzio','Obie','Odell','Odie','Odis','Olan','Olen','Olin','Oliver','Ollie','Omar','Omer','Oneal','Ora','Oral','Oran','Oren','Orin','Orland','Orlando','Orrin','Orval','Orvil','Orville','Oscar','Oswald','Otha','Otho','Otis','Ottis','Otto','Owen','Pablo','Palmer','Parker','Pasquale','Pat','Patrick','Patsy','Paul','Pearl','Pedro','Percy','Perry','Pete','Peter','Phil','Philip','Phillip','Pierce','Pierre','Porter','Preston','Prince','Quentin','Quinton','Rafael','Raleigh','Ralph','Ramiro','Ramon','Randall','Randolph','Raphael','Raul','Ray','Rayford','Raymon','Raymond','Reece','Reed','Reginald','Regis','Reid','Rene','Reno','Reuben','Rex','Reynaldo','Reynold','Ricardo','Richard','Richmond','Riley','Robert','Roberto','Rocco','Roderick','Rodger','Rodney','Rodolfo','Roger','Rogers','Roland','Rolland','Rollin','Roman','Romeo','Ronald','Roosevelt','Rosario','Roscoe','Rosevelt','Ross','Rowland','Roy','Royal','Royce','Ruben','Rubin','Ruby','Rudolph','Rudy','Rueben','Rufus','Rupert','Russel','Russell','Ruth','Salvador','Salvatore','Sam','Sammie','Sammy','Samuel','Sandy','Sanford','Santiago','Santo','Santos','Saul','Scott','Sebastian','Seth','Seymour','Shelby','Sheldon','Shelton','Sherman','Sherwood','Shirley','Sidney','Sigmund','Silas','Silvio','Simon','Smith','Sol','Solomon','Spencer','Stacy','Stanford','Stanley','Stanton','Stephen','Sterling','Steve','Steven','Stewart','Stuart','Sumner','Sydney','Sylvan','Sylvester','Talmadge','Talmage','Taylor','Ted','Teddy','Terrence','Terry','Thad','Thaddeus','Theadore','Theo','Theodore','Theron','Thomas','Thornton','Thurman','Thurston','Tillman','Timothy','Tom','Tomas','Tommie','Tommy','Tony','Tracy','Travis','Trinidad','Troy','Truman','Turner','Ulysses','Urban','Valentine','Van','Vance','Vaughn','Verl','Verle','Verlin','Vern','Verne','Verner','Vernie','Vernon','Vester','Vicente','Victor','Vincent','Virgil','Virgle','Vito','Vivian','Wade','Waldo','Walker','Wallace','Walter','Walton','Ward','Wardell','Warner','Warren','Watson','Wayland','Wayne','Webster','Weldon','Wellington','Welton','Wendell','Werner','Wesley','Wilber','Wilbert','Wilbur','Wilburn','Wiley','Wilford','Wilfred','Wilfrid','Will','Willam','Willard','William','Williams','Willian','Willie','Willis','Wilmer','Wilson','Wilton','Winfield','Winford','Winfred','Winston','Winton','Wm','Woodrow','Worth','Wylie','Wyman','Yoshio','Zack','Zane']
DATE_START = datetime.datetime.now()
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_DELTA = 365
STRING_SIZE = 40
INT_START = 0
INT_END = 100
GENDER_LIST = ['F', 'M']

# Arguments
ENCLOSER = ''
DELIMITER = ','
ROWS = 10
TEXT = 'index; uuid; firstname; lastname; int::start=18,end=95; date::delta=365'
OUTPUT = ''
CHUNK_SIZE = 100000

# Global
gender = None

class FabDate:
    def __init__(self, start, delta, format, seed):
        self.rd = random.Random()
        if seed is not None:
            self.rd.seed(int(seed))
        self.start = start
        self.delta = int(delta)
        self.format = format
        self.today = DATE_START if self.start is None else datetime.datetime.strptime(self.start, '%Y-%m-%d').date()

    def generator(self):
        date = self.today + datetime.timedelta(self.rd.randint(-1 * self.delta, self.delta))

        hour = self.rd.randint(0, 23)
        minute = self.rd.randint(0, 59)
        second = self.rd.randint(0, 59)
        millis = self.rd.randint(0, 999999)

        yield datetime.datetime.combine(date, datetime.time(hour, minute, second, millis)).strftime(self.format)

class FabConstant:
    def __init__(self, value):
        self.value = value

    def generator(self):
        yield self.value

class FabIndex:
    def __init__(self, start):
        self.counter = itertools.count(int(start))

    def generator(self):
        yield next(self.counter)

class FabUUID:
    def __init__(self, seed):
        self.rd = random.Random()
        if seed is not None:
            self.rd.seed(int(seed))

    def generator(self):
        yield uuid.UUID(int=self.rd.getrandbits(128), version=4)

class FabInt:
    def __init__(self, start, end, seed):
        self.rd = random.Random()
        self.start = int(start)
        self.end = int(end)
        if seed is not None:
            self.rd.seed(int(seed))

    def generator(self):
        yield self.rd.randint(self.start, self.end)

class FabString:
    def __init__(self, size, seed):
        self.rd = random.Random()
        self.size = int(size)
        if seed is not None:
            self.rd.seed(int(seed))

    def generator(self):
        yield ''.join(self.rd.choice(string.ascii_letters + string.digits) for x in range(self.size))

class FabChoices:
    def __init__(self, choices, weights, seed):
        self.rd = random.Random()
        self.choices = choices
        if weights is not None:
            self.weights = [float(x) for x in weights.split(' ')]
        else:
            self.weights = None
        if seed is not None:
            self.rd.seed(int(seed))

    def generator(self):
        yield self.rd.choices(self.choices, weights=self.weights, k=1)[0]

class FabLastName:
    def __init__(self, seed):
        self.rd = random.Random()
        if seed is not None:
            self.rd.seed(int(seed))

    def generator(self):
        yield self.rd.choice(LASTNAME)

class FabTel:
    def __init__(self, seed):
        self.rd = random.Random()
        if seed is not None:
            self.rd.seed(int(seed))

    def generator(self):
        yield '(' + f'{self.rd.randint(100, 999):03}' + ') ' + f'{self.rd.randint(1, 999):03}' + '-' + f'{self.rd.randint(1, 9999):04}'

class FabSSN:
    def __init__(self, seed):
        self.rd = random.Random()
        if seed is not None:
            self.rd.seed(int(seed))

    def generator(self):
        yield f'{self.rd.randint(1, 999):03}' + '-' + f'{self.rd.randint(1, 99):02}' + '-' + f'{self.rd.randint(1, 9999):04}'

class FabFirstName:
    def __init__(self, gndr, seed):
        self.rd = random.Random()
        global gender
        self.gender = gender
        if gndr is not None:
            if gndr == 'f':
                self.gender = 0
                gender = 0
            else:
                self.gender = 1
                gender = 1
        if seed is not None:
            self.rd.seed(int(seed))
        
    def generator(self):
        global gender
        if self.gender is None:
            # 0 = female, 1 = male
            if self.rd.randint(0, 1):
                gender = 0
                yield self.rd.choice(FEMALE_NAMES)
            else:
                gender = 1
                yield self.rd.choice(MALE_NAMES)

        elif self.gender == 0:
            yield self.rd.choice(FEMALE_NAMES)
        else:
            yield self.rd.choice(MALE_NAMES) 
   
class FabGender:
    def __init__(self, seed):
        self.rd = random.Random()
        if seed is not None:
            self.rd.seed(int(seed))
        
    def generator(self):
        yield self.rd.choice(GENDER_LIST) if gender is None else GENDER_LIST[int(gender)]

def get_fields(text):
    fields = [x.strip().split("::") for x in text.split(';')]

    for f in fields:
        if len(f) == 2:
            f[1] = {k.strip(): v.strip() for k, v in (x.split('=') for x in f[1].split(','))}
        else:
            f.append({})

        if f[0] == 'int':
            f[1] = FabInt(f[1].get('start', INT_START), f[1].get('end', INT_END), f[1].get('seed', None))
        
        elif f[0] == 'index':
            f[1] = FabIndex(f[1].get('start', 1))
        
        elif f[0] == 'constant':
            f[1] = FabConstant(f[1].get('value', None))

        elif f[0] == 'uuid':
            f[1] = FabUUID(f[1].get('seed', None))
        
        elif f[0] == 'ssn':
            f[1] = FabSSN(f[1].get('seed', None))
        
        elif f[0] == 'tel':
            f[1] = FabTel(f[1].get('seed', None))

        elif f[0] == 'lastname':
            f[1] = FabLastName(f[1].get('seed', None))

        elif f[0] == 'date':
            f[1] = FabDate(f[1].get('start', None), f[1].get('delta', DATE_DELTA), f[1].get('format', DATE_FORMAT), f[1].get('seed', None))
        
        elif f[0] == 'choices':
            f[1] = FabChoices(f[1]['list'].split(" "), f[1].get('weights', None), f[1].get('seed', None))

        elif f[0] == 'string':
            f[1] = FabString(f[1].get('size', STRING_SIZE), f[1].get('seed', None))

        elif f[0] == 'gender':
            f[1] = FabGender(f[1].get('seed', None))

        elif f[0] == 'firstname':
            f[1] = FabFirstName(f[1].get('gender', None), f[1].get('seed', None))

        else:
            pass

    return tuple(fields)

def carota(rows=ROWS, 
            text=TEXT, 
            delimiter=DELIMITER, 
            encloser=ENCLOSER, 
            output=OUTPUT, 
            chunk_size=CHUNK_SIZE):
    
    fields = get_fields(text)

    for _ in range(rows):
        yield delimiter.join([f'{encloser}{x}{encloser}' for x in [next(f[1].generator()) for f in fields]])
