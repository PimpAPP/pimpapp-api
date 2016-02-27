/*
INSERT INTO auth_user VALUES(1,'pbkdf2_sha256$20000$8rPeln1kYJWz$so4XVqVp6BgNuOcvnzg+lZpBIrcPYfWoeYephQLDxrY=',1,'admin','','','admin@admin.cc',1,1,'2016-01-27 11:04:02.305960',NULL);
*/

INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (1, "Rafael dos Santos", 0, "Rua Dos Gusmões, 500", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (2, "Rodrigue Lucena", 0, "Av Liberdade 163", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (3, "Gabriel dos Santos", 0, "Rua Ferreira de Araújo", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (4, "Denilson", 0, "Rua Cardeal Arco Verde 1000", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (5, "Jorge Natalino", 0, "Rua Rodesia 220", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (6, "Nego", 0, "Rua Belmiro Braga n 216", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (7, "Fábio", 0, "Rua Harmonia 71", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (8, "Buiu", 0, "Rua Pedroso de Moraes 1280", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (9, "Marco Viana dos Santos", 0, "Rua Arthur de Azevedo n 550", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (10, "Biro-Biro", 0, "Av Faria Lima 2200", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (11, "Sergio Bispo", 0, "Rua Glicerio 123", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (12, "Fernando Miguel", 0, "Metrô Armênia", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (13, "Marquinhos", 0, "Av Rebouças 3000", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (14, "Priscila", 0, "Av. Roberto Marinho 1550", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (15, "Jose Teixeira Dantas", 0, "R. Barão de Paranapiacaba", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (16, "Denilson", 0, "Rua Inacio Pereira da Rocha n 25", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_carroceiro (id, name, is_locked, address_base, catador_type, has_motor_vehicle, carroca_pimpada, moderation_status, created_on) VALUES (17, "Jose Parque do Gato", 0, "Rua Newtom Prado n 500", 0, 0, "C", 'A', '2016-01-27 10:56:13.121701');

INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (1, "Rua Dos Gusmões, 500", -23.5374089, -46.6399287, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (2, "Av Liberdade 163", -23.5544961, -46.6354377, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (3, "Rua Ferreira de Araújo", -23.5577321, -46.6973732, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (4, "Rua Cardeal Arco Verde 1000", -23.5577372, -46.6817867, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (5, "Rua Rodesia 220", -23.5513181, -46.6907592, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (6, "Rua Belmiro Braga n 216", -23.55757172, -46.68607322, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (7, "Rua Harmonia 71", -23.5571661, -46.6867196, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (8, "Rua Pedroso de Moraes 1280", -23.5599579, -46.693902, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (9, "Rua Arthur de Azevedo n 550", -23.5600974, -46.6774287, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (10, "Av Faria Lima 2200", -23.5755786, -46.6876801, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (11, "Rua Glicerio 123", -23.5529011, -46.6276388, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (12, "Metrô Armênia", -23.525545, -46.629317, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (13, "Av Rebouças 3000", -23.5696463, -46.6882664, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (14, "Av. Roberto Marinho 1550", -23.6186647, -46.6832331, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (15, "R. Barão de Paranapiacaba", -23.5494343, -46.6338535, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (16, "Rua Inacio Pereira da Rocha n 25", -23.5586191, -46.6872522, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_latitudelongitude (carroceiro_id, reverse_geocoding, latitude, longitude, moderation_status, created_on) VALUES (17, "Rua Newtom Prado n 500", -23.5226943, -46.6405354, 'A', '2016-01-27 10:56:13.121701');

INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (1,  "982416387", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (2,  "984357774", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (3,  "954861273", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (4,  "954167784", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (5,  "943270892", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (6,  "967847079", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (7,  "988412088", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (8,  "989083725", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (9,  "975004604", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (10, "977399129", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (11, "962270116", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (12, "948867162", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (13, "957207459", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (14, "964579284", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (15, "972059149", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (16, "954167784", 0, 'A', '2016-01-27 10:56:13.121701');
INSERT INTO api_phone (carroceiro_id, phone, has_whatsapp, moderation_status, created_on) VALUES (17, "984678922", 0, 'A', '2016-01-27 10:56:13.121701');
