# prefijos_paises.py
# Prefijos ITU de radioaficionado → país
# Ordenados de más largo a más corto para que los específicos tengan prioridad
# Fuente: ITU Table of Allocation of International Call Sign Series + ARRL DXCC list

PREFIJOS = [
    # -------------------------------------------------------------------------
    # EUROPA
    # -------------------------------------------------------------------------
    # España
    ('EA8', 'Canary Islands'), ('EA9', 'Ceuta & Melilla'),
    ('EB8', 'Canary Islands'), ('EB9', 'Ceuta & Melilla'),
    ('EA', 'Spain'), ('EB', 'Spain'), ('EC', 'Spain'), ('ED', 'Spain'),
    ('EE', 'Spain'), ('EF', 'Spain'), ('EG', 'Spain'), ('EH', 'Spain'),
    # Portugal
    ('CQ8', 'Azores'), ('CR3', 'Madeira'), ('CS3', 'Madeira'),
    ('CU', 'Azores'), ('CT3', 'Madeira'),
    ('CT', 'Portugal'), ('CQ', 'Portugal'), ('CS', 'Portugal'),
    # Francia
    ('FG', 'Guadeloupe'), ('FH', 'Mayotte'), ('FM', 'Martinique'),
    ('FO', 'French Polynesia'), ('FP', 'St. Pierre & Miquelon'),
    ('FR', 'Reunion'), ('FS', 'St. Martin'), ('FW', 'Wallis & Futuna'),
    ('FY', 'French Guiana'),
    ('F', 'France'), ('TM', 'France'),
    # Alemania
    ('DA', 'Germany'), ('DB', 'Germany'), ('DC', 'Germany'), ('DD', 'Germany'),
    ('DE', 'Germany'), ('DF', 'Germany'), ('DG', 'Germany'), ('DH', 'Germany'),
    ('DI', 'Germany'), ('DJ', 'Germany'), ('DK', 'Germany'), ('DL', 'Germany'),
    ('DM', 'Germany'), ('DN', 'Germany'), ('DO', 'Germany'), ('DP', 'Germany'),
    ('DQ', 'Germany'), ('DR', 'Germany'),
    # Italia
    ('IS', 'Sardinia'), ('IT', 'Sicily'),
    ('I', 'Italy'), ('IK', 'Italy'), ('IQ', 'Italy'), ('IR', 'Italy'),
    ('IU', 'Italy'), ('IV', 'Italy'), ('IW', 'Italy'), ('IX', 'Italy'), ('IZ', 'Italy'),
    # Reino Unido
    ('2E', 'England'), ('2M', 'Scotland'), ('2W', 'Wales'), ('2I', 'Northern Ireland'),
    ('GI', 'Northern Ireland'), ('GJ', 'Jersey'), ('GU', 'Guernsey'),
    ('GM', 'Scotland'), ('GS', 'Scotland'), ('GW', 'Wales'), ('GD', 'Isle of Man'),
    ('MI', 'Northern Ireland'), ('MJ', 'Jersey'), ('MU', 'Guernsey'),
    ('MM', 'Scotland'), ('MW', 'Wales'), ('MD', 'Isle of Man'),
    ('G', 'England'), ('M', 'England'),
    # Países Bajos
    ('PA', 'Netherlands'), ('PB', 'Netherlands'), ('PC', 'Netherlands'),
    ('PD', 'Netherlands'), ('PE', 'Netherlands'), ('PF', 'Netherlands'),
    ('PG', 'Netherlands'), ('PH', 'Netherlands'), ('PI', 'Netherlands'),
    ('PJ', 'Netherlands Antilles'),
    # Bélgica
    ('ON', 'Belgium'), ('OO', 'Belgium'), ('OR', 'Belgium'), ('OS', 'Belgium'), ('OT', 'Belgium'),
    # Suiza
    ('HB', 'Switzerland'), ('HE', 'Switzerland'),
    # Liechtenstein
    ('HB0', 'Liechtenstein'),
    # Austria
    ('OE', 'Austria'),
    # República Checa
    ('OK', 'Czech Republic'), ('OL', 'Czech Republic'),
    # Eslovaquia
    ('OM', 'Slovak Republic'),
    # Polonia
    ('SN', 'Poland'), ('SO', 'Poland'), ('SP', 'Poland'), ('SQ', 'Poland'), ('SR', 'Poland'),
    # Hungría
    ('HA', 'Hungary'), ('HG', 'Hungary'),
    # Rumanía
    ('YO', 'Romania'), ('YP', 'Romania'), ('YQ', 'Romania'), ('YR', 'Romania'),
    # Bulgaria
    ('LZ', 'Bulgaria'),
    # Serbia
    ('YT', 'Serbia'), ('YU', 'Serbia'),
    # Croacia
    ('9A', 'Croatia'),
    # Eslovenia
    ('S5', 'Slovenia'),
    # Bosnia-Herzegovina
    ('E7', 'Bosnia-Herzegovina'),
    # Macedonia del Norte
    ('Z3', 'North Macedonia'),
    # Montenegro
    ('4O', 'Montenegro'),
    # Kosovo
    ('Z6', 'Kosovo'),
    # Albania
    ('ZA', 'Albania'),
    # Grecia
    ('SV', 'Greece'), ('SW', 'Greece'), ('SX', 'Greece'), ('SY', 'Greece'), ('SZ', 'Greece'),
    # Chipre
    ('5B', 'Cyprus'), ('C4', 'Cyprus'),
    # Malta
    ('9H', 'Malta'),
    # Finlandia
    ('OF', 'Finland'), ('OG', 'Finland'), ('OH', 'Finland'), ('OI', 'Finland'),
    # Noruega
    ('LA', 'Norway'), ('LB', 'Norway'), ('LC', 'Norway'), ('LD', 'Norway'),
    ('LE', 'Norway'), ('LF', 'Norway'), ('LG', 'Norway'), ('LH', 'Norway'),
    ('LI', 'Norway'), ('LJ', 'Norway'), ('LK', 'Norway'), ('LL', 'Norway'),
    ('LM', 'Norway'), ('LN', 'Norway'),
    # Suecia
    ('SA', 'Sweden'), ('SB', 'Sweden'), ('SC', 'Sweden'), ('SD', 'Sweden'),
    ('SE', 'Sweden'), ('SF', 'Sweden'), ('SG', 'Sweden'), ('SH', 'Sweden'),
    ('SI', 'Sweden'), ('SJ', 'Sweden'), ('SK', 'Sweden'), ('SL', 'Sweden'), ('SM', 'Sweden'),
    # Dinamarca
    ('OU', 'Denmark'), ('OV', 'Denmark'), ('OW', 'Denmark'), ('OX', 'Greenland'),
    ('OY', 'Faroe Islands'), ('OZ', 'Denmark'),
    # Islandia
    ('TF', 'Iceland'),
    # Irlanda
    ('EI', 'Ireland'), ('EJ', 'Ireland'),
    # Estonia
    ('ES', 'Estonia'),
    # Letonia
    ('YL', 'Latvia'),
    # Lituania
    ('LY', 'Lithuania'),
    # Bielorrusia
    ('EU', 'Belarus'), ('EV', 'Belarus'), ('EW', 'Belarus'),
    # Ucrania
    ('EM', 'Ukraine'), ('EN', 'Ukraine'), ('EO', 'Ukraine'),
    ('UR', 'Ukraine'), ('US', 'Ukraine'), ('UT', 'Ukraine'), ('UU', 'Ukraine'),
    ('UV', 'Ukraine'), ('UW', 'Ukraine'), ('UX', 'Ukraine'), ('UY', 'Ukraine'), ('UZ', 'Ukraine'),
    # Moldavia
    ('ER', 'Moldova'),
    # Rusia (UA1-UA9, RA-RZ)
    ('UA', 'Russia'), ('UB', 'Russia'), ('UC', 'Russia'), ('UD', 'Russia'),
    ('UE', 'Russia'), ('UF', 'Russia'), ('UG', 'Russia'), ('UH', 'Russia'), ('UI', 'Russia'),
    ('RA', 'Russia'), ('RB', 'Russia'), ('RC', 'Russia'), ('RD', 'Russia'), ('RE', 'Russia'),
    ('RF', 'Russia'), ('RG', 'Russia'), ('RH', 'Russia'), ('RI', 'Russia'), ('RJ', 'Russia'),
    ('RK', 'Russia'), ('RL', 'Russia'), ('RM', 'Russia'), ('RN', 'Russia'), ('RO', 'Russia'),
    ('RP', 'Russia'), ('RQ', 'Russia'), ('RR', 'Russia'), ('RS', 'Russia'), ('RT', 'Russia'),
    ('RU', 'Russia'), ('RV', 'Russia'), ('RW', 'Russia'), ('RX', 'Russia'), ('RY', 'Russia'),
    ('RZ', 'Russia'), ('R', 'Russia'),
    # Luxemburgo
    ('LX', 'Luxembourg'),
    # Andorra
    ('C3', 'Andorra'),
    # Mónaco
    ('3A', 'Monaco'),
    # San Marino
    ('T7', 'San Marino'),
    # Ciudad del Vaticano
    ('HV', 'Vatican'),
    # Gibraltar
    ('ZB', 'Gibraltar'),
    # -------------------------------------------------------------------------
    # ORIENTE MEDIO / ASIA OCCIDENTAL
    # -------------------------------------------------------------------------
    # Turquía
    ('TA', 'Turkey'), ('TB', 'Turkey'), ('TC', 'Turkey'), ('YM', 'Turkey'),
    # Israel
    ('4X', 'Israel'), ('4Z', 'Israel'),
    # Jordania
    ('JY', 'Jordan'),
    # Líbano
    ('OD', 'Lebanon'),
    # Siria
    ('YK', 'Syria'),
    # Irak
    ('YI', 'Iraq'),
    # Irán
    ('EP', 'Iran'), ('EQ', 'Iran'),
    # Arabia Saudita
    ('HZ', 'Saudi Arabia'), ('7Z', 'Saudi Arabia'),
    # Emiratos Árabes
    ('A6', 'UAE'),
    # Kuwait
    ('9K', 'Kuwait'),
    # Qatar
    ('A7', 'Qatar'),
    # Bahrein
    ('A9', 'Bahrain'),
    # Omán
    ('A4', 'Oman'),
    # Yemen
    ('7O', 'Yemen'),
    # Afganistán
    ('T6', 'Afghanistan'), ('YA', 'Afghanistan'),
    # Pakistán
    ('AP', 'Pakistan'), ('AQ', 'Pakistan'), ('AR', 'Pakistan'), ('AS', 'Pakistan'),
    # -------------------------------------------------------------------------
    # ASIA
    # -------------------------------------------------------------------------
    # India
    ('VU', 'India'), ('AT', 'India'), ('AU', 'India'), ('AV', 'India'), ('AW', 'India'),
    # Sri Lanka
    ('4S', 'Sri Lanka'),
    # Bangladesh
    ('S2', 'Bangladesh'), ('S3', 'Bangladesh'),
    # Nepal
    ('9N', 'Nepal'),
    # Bután
    ('A5', 'Bhutan'),
    # Maldivas
    ('8Q', 'Maldives'),
    # Myanmar
    ('XY', 'Myanmar'), ('XZ', 'Myanmar'),
    # Tailandia
    ('HS', 'Thailand'), ('E2', 'Thailand'),
    # Vietnam
    ('3W', 'Vietnam'), ('XV', 'Vietnam'),
    # Camboya
    ('XU', 'Cambodia'),
    # Laos
    ('XW', 'Laos'),
    # Malasia
    ('9M', 'Malaysia'),
    # Singapur
    ('9V', 'Singapore'),
    # Indonesia
    ('YB', 'Indonesia'), ('YC', 'Indonesia'), ('YD', 'Indonesia'), ('YE', 'Indonesia'),
    ('YF', 'Indonesia'), ('YG', 'Indonesia'), ('YH', 'Indonesia'),
    # Filipinas
    ('DU', 'Philippines'), ('DV', 'Philippines'), ('DW', 'Philippines'), ('DX', 'Philippines'),
    # Brunei
    ('V8', 'Brunei'),
    # Timor Oriental
    ('4W', 'East Timor'),
    # Japón
    ('JA', 'Japan'), ('JE', 'Japan'), ('JF', 'Japan'), ('JG', 'Japan'),
    ('JH', 'Japan'), ('JI', 'Japan'), ('JJ', 'Japan'), ('JK', 'Japan'),
    ('JL', 'Japan'), ('JM', 'Japan'), ('JN', 'Japan'), ('JO', 'Japan'),
    ('JP', 'Japan'), ('JQ', 'Japan'), ('JR', 'Japan'), ('JS', 'Japan'),
    # China
    ('BA', 'China'), ('BD', 'China'), ('BG', 'China'), ('BH', 'China'),
    ('BI', 'China'), ('BJ', 'China'), ('BK', 'China'), ('BL', 'China'),
    ('BM', 'China'), ('BN', 'China'), ('BO', 'China'), ('BP', 'China'),
    ('BQ', 'China'), ('BR', 'China'), ('BS', 'China'), ('BT', 'China'),
    ('BU', 'China'), ('BV', 'China'), ('BW', 'China'), ('BX', 'China'),
    ('BY', 'China'), ('BZ', 'China'),
    # Hong Kong
    ('VR', 'Hong Kong'),
    # Macao
    ('XX', 'Macao'),
    # Taiwan
    ('BV', 'Taiwan'),
    # Corea del Sur
    ('DS', 'South Korea'), ('DT', 'South Korea'), ('HL', 'South Korea'),
    # Corea del Norte
    ('HM', 'North Korea'), ('P5', 'North Korea'),
    # Mongolia
    ('JT', 'Mongolia'), ('JU', 'Mongolia'), ('JV', 'Mongolia'),
    # Kazajistán
    ('UN', 'Kazakhstan'), ('UO', 'Kazakhstan'),
    # Uzbekistán
    ('UK', 'Uzbekistan'),
    # Turkmenistán
    ('EZ', 'Turkmenistan'),
    # Tayikistán
    ('EY', 'Tajikistan'),
    # Kirguistán
    ('EX', 'Kyrgyzstan'),
    # Azerbaiyán
    ('4J', 'Azerbaijan'), ('4K', 'Azerbaijan'),
    # Armenia
    ('EK', 'Armenia'),
    # Georgia
    ('4L', 'Georgia'),
    # -------------------------------------------------------------------------
    # ÁFRICA
    # -------------------------------------------------------------------------
    # Marruecos
    ('CN', 'Morocco'),
    # Argelia
    ('7R', 'Algeria'), ('7S', 'Algeria'), ('7T', 'Algeria'), ('7U', 'Algeria'),
    ('7V', 'Algeria'), ('7W', 'Algeria'), ('7X', 'Algeria'),
    # Túnez
    ('3V', 'Tunisia'), ('TS', 'Tunisia'),
    # Libia
    ('5A', 'Libya'),
    # Egipto
    ('SU', 'Egypt'),
    # Sudán
    ('ST', 'Sudan'),
    # Etiopía
    ('ET', 'Ethiopia'),
    # Somalia
    ('T5', 'Somalia'),
    # Kenia
    ('5Z', 'Kenya'),
    # Tanzania
    ('5H', 'Tanzania'),
    # Uganda
    ('5X', 'Uganda'),
    # Ruanda
    ('9X', 'Rwanda'),
    # Burundi
    ('9U', 'Burundi'),
    # Nigeria
    ('5N', 'Nigeria'),
    # Ghana
    ('9G', 'Ghana'),
    # Senegal
    ('6V', 'Senegal'), ('6W', 'Senegal'),
    # Costa de Marfil
    ('TU', 'Ivory Coast'),
    # Camerún
    ('TJ', 'Cameroon'),
    # Congo (Rep. Dem.)
    ('9O', 'DR Congo'), ('9P', 'DR Congo'), ('9Q', 'DR Congo'), ('9R', 'DR Congo'),
    # Congo (Rep.)
    ('TN', 'Republic of Congo'),
    # Angola
    ('D3', 'Angola'),
    # Mozambique
    ('C9', 'Mozambique'),
    # Zambia
    ('9J', 'Zambia'),
    # Zimbabwe
    ('Z2', 'Zimbabwe'),
    # Botswana
    ('A2', 'Botswana'),
    # Namibia
    ('V5', 'Namibia'),
    # Sudáfrica
    ('ZR', 'South Africa'), ('ZS', 'South Africa'), ('ZT', 'South Africa'), ('ZU', 'South Africa'),
    # Madagascar
    ('5R', 'Madagascar'),
    # Mauricio
    ('3B', 'Mauritius'),
    # Reunión (Francia)
    ('FR', 'Reunion'),
    # Islas Canarias → ya cubierto arriba
    # -------------------------------------------------------------------------
    # NORTEAMÉRICA
    # -------------------------------------------------------------------------
    # Estados Unidos
    ('K', 'United States'), ('N', 'United States'), ('W', 'United States'),
    ('AA', 'United States'), ('AB', 'United States'), ('AC', 'United States'),
    ('AD', 'United States'), ('AE', 'United States'), ('AF', 'United States'),
    ('AG', 'United States'), ('AH', 'United States'), ('AI', 'United States'),
    ('AJ', 'United States'), ('AK', 'United States'),
    # Canadá
    ('VA', 'Canada'), ('VB', 'Canada'), ('VC', 'Canada'), ('VE', 'Canada'),
    ('VF', 'Canada'), ('VG', 'Canada'), ('VO', 'Canada'), ('VY', 'Canada'),
    # México
    ('XE', 'Mexico'), ('XF', 'Mexico'), ('XG', 'Mexico'), ('XH', 'Mexico'), ('XI', 'Mexico'),
    # Guatemala
    ('TG', 'Guatemala'),
    # Belice
    ('V3', 'Belize'),
    # Honduras
    ('HR', 'Honduras'), ('HQ', 'Honduras'),
    # El Salvador
    ('YS', 'El Salvador'),
    # Nicaragua
    ('YN', 'Nicaragua'), ('H6', 'Nicaragua'), ('H7', 'Nicaragua'),
    # Costa Rica
    ('TI', 'Costa Rica'),
    # Panamá
    ('HP', 'Panama'),
    # Cuba
    ('CM', 'Cuba'), ('CO', 'Cuba'), ('T4', 'Cuba'),
    # Jamaica
    ('6Y', 'Jamaica'),
    # Haití
    ('HH', 'Haiti'),
    # República Dominicana
    ('HI', 'Dominican Republic'),
    # Puerto Rico
    ('KP4', 'Puerto Rico'), ('NP4', 'Puerto Rico'), ('WP4', 'Puerto Rico'),
    # Bahamas
    ('C6', 'Bahamas'),
    # Trinidad y Tobago
    ('9Y', 'Trinidad & Tobago'), ('9Z', 'Trinidad & Tobago'),
    # Barbados
    ('8P', 'Barbados'),
    # -------------------------------------------------------------------------
    # SUDAMÉRICA
    # -------------------------------------------------------------------------
    # Brasil
    ('PP', 'Brazil'), ('PQ', 'Brazil'), ('PR', 'Brazil'), ('PS', 'Brazil'),
    ('PT', 'Brazil'), ('PU', 'Brazil'), ('PV', 'Brazil'), ('PW', 'Brazil'),
    ('PX', 'Brazil'), ('PY', 'Brazil'), ('PZ', 'Suriname'),
    # Argentina
    ('LO', 'Argentina'), ('LP', 'Argentina'), ('LQ', 'Argentina'), ('LR', 'Argentina'),
    ('LS', 'Argentina'), ('LT', 'Argentina'), ('LU', 'Argentina'), ('LV', 'Argentina'),
    ('LW', 'Argentina'),
    # Chile
    ('CA', 'Chile'), ('CB', 'Chile'), ('CC', 'Chile'), ('CD', 'Chile'), ('CE', 'Chile'),
    ('XQ', 'Chile'), ('XR', 'Chile'),
    # Uruguay
    ('CV', 'Uruguay'), ('CW', 'Uruguay'),
    # Paraguay
    ('ZP', 'Paraguay'),
    # Bolivia
    ('CP', 'Bolivia'),
    # Perú
    ('OA', 'Peru'), ('OB', 'Peru'), ('OC', 'Peru'),
    # Ecuador
    ('HC', 'Ecuador'), ('HD', 'Ecuador'),
    # Colombia
    ('HJ', 'Colombia'), ('HK', 'Colombia'),
    # Venezuela
    ('YV', 'Venezuela'), ('YW', 'Venezuela'), ('YX', 'Venezuela'), ('YY', 'Venezuela'),
    # Guyana
    ('8R', 'Guyana'),
    # Surinam → PZ arriba
    # -------------------------------------------------------------------------
    # OCEANÍA
    # -------------------------------------------------------------------------
    # Australia
    ('VK', 'Australia'),
    # Nueva Zelanda
    ('ZL', 'New Zealand'), ('ZM', 'New Zealand'),
    # Papua Nueva Guinea
    ('P2', 'Papua New Guinea'),
    # Islas Salomón
    ('H44', 'Solomon Islands'),
    # Vanuatu
    ('YJ', 'Vanuatu'),
    # Fiyi
    ('3D2', 'Fiji'),
    # Tonga
    ('A3', 'Tonga'),
    # Samoa
    ('5W', 'Samoa'),
    # Samoa Americana
    ('KH8', 'American Samoa'),
    # Hawái
    ('KH6', 'Hawaii'), ('NH6', 'Hawaii'), ('WH6', 'Hawaii'),
    # Guam
    ('KH2', 'Guam'), ('NH2', 'Guam'), ('WH2', 'Guam'),
    # Islas Marianas del Norte
    ('KH0', 'Mariana Islands'),
    # Islas Marshall
    ('V7', 'Marshall Islands'),
    # Micronesia
    ('V6', 'Micronesia'),
    # Palau
    ('T8', 'Palau'),
    # Nauru
    ('C2', 'Nauru'),
    # Kiribati
    ('T30', 'West Kiribati'), ('T31', 'Central Kiribati'), ('T32', 'East Kiribati'),
]
