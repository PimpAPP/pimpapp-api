/*
INSERT INTO auth_user VALUES(1,'pbkdf2_sha256$20000$8rPeln1kYJWz$so4XVqVp6BgNuOcvnzg+lZpBIrcPYfWoeYephQLDxrY=',1,'admin','','','admin@admin.cc',1,1,'2016-01-27 11:04:02.305960',NULL);
*/

INSERT INTO api_carroceiro (id, name, phone, type) VALUES (1, "Rafael dos Santos", "982416387", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (2, "Rodrigue Lucena", "984357774", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (3, "Gabriel dos Santos", "954861273", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (4, "Denilson", "954167784", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (5, "Jorge Natalino", "943270892", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (6, "Nego", "967847079", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (7, "Fábio", "988412088", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (8, "Buiu", "989083725", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (9, "Marco Viana dos Santos","975004604", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (10, "Biro-Biro", "977399129", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (11, "Sergio Bispo", "962270116", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (12, "Fernando Miguel", "948867162", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (13, "Marquinhos", "957207459", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (14, "Priscila", "964579284", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (15, "Jose Teixeira Dantas", "972059149", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (16, "Denilson", "954167784", "C");
INSERT INTO api_carroceiro (id, name, phone, type) VALUES (17, "Jose Parque do Gato", "984678922", "C");

INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 1, "Rua Dos Gusmões, 500", -23.5374089, -46.6399287, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 2, "Av Liberdade 163", -23.5544961, -46.6354377, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 3, "Rua Ferreira de Araújo", -23.5577321, -46.6973732, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 4, "Rua Cardeal Arco Verde 1000", -23.5577372, -46.6817867, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 5, "Rua Rodesia 220", -23.5513181, -46.6907592, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 6, "Rua Belmiro Braga n 216", -23.55757172, -46.68607322, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 7, "Rua Harmonia 71", -23.5571661, -46.6867196, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 8, "Rua Pedroso de Moraes 1280", -23.5599579, -46.693902, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 9, "Rua Arthur de Azevedo n 550", -23.5600974, -46.6774287, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 10, "Av Faria Lima 2200", -23.5755786, -46.6876801, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 11, "Rua Glicerio 123", -23.5529011, -46.6276388, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 12, "Metrô Armênia", -23.525545, -46.629317, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 13, "Av Rebouças 3000", -23.5696463, -46.6882664, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 14, "Av. Roberto Marinho 1550", -23.6186647, -46.6832331, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 15, "R. Barão de Paranapiacaba", -23.5494343, -46.6338535, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 16, "Rua Inacio Pereira da Rocha n 25", -23.5586191, -46.6872522, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (user_id, carroceiro_id, address, latitude, longitude, moderation_status, created_on) VALUES (1, 17, "Rua Newtom Prado n 500", -23.5226943, -46.6405354, 'A', '2016-01-27 10:56:13.121701');