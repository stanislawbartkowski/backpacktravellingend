drop table if exists trips cascade;
drop table if exists users cascade ;
drop table if exists payments cascade;
drop table if exists chats cascade;
drop table if exists photos cascade;
drop table if exists trip_participant cascade;
drop table if exists friends cascade;
drop table if exists membership_status cascade;
drop table if exists ground_transportation cascade;
drop table if exists ground_transportation_reservations cascade;
drop table if exists ground_transportation_ticket cascade;
drop table if exists flights cascade;
drop table if exists flights_reservations cascade;
drop table if exists flights_reservations_ticket cascade;
drop table if exists stays cascade;
drop table if exists stays_reservations cascade;
drop table if exists rooms cascade;
drop table if exists made_payments cascade;

CREATE TABLE trips (
    PK_TRIPS INT PRIMARY key GENERATED ALWAYS AS IDENTITY,
    name varchar,
    location varchar,
    start_time timestamp,
    end_time timestamp,
    flights varchar,
    stays varchar,
    transportation varchar,
    activities varchar,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

create table users (
   PK_USERS INT primary key GENERATED ALWAYS AS IDENTITY,
   name varchar,
   email varchar,
   email_verified_at timestamp,
   password varchar,
   remember_token varchar,
   created_at timestamp NOT NULL,
   updated_at timestamp NOT NULL,
   phone_number varchar,
   description varchar,
   profile_image varchar,
   countries int
);

create table payments (
	PK_PAYMENTS int primary key generated always as identity,
	user_id int not null,
	constraint fk_users
	foreign key(user_id)
	references users(pk_users),
	splitwise varchar
);

create table chats (
	sender int not null,
	receiver int not null,
	message varchar,
	sequence_number int not null,
	
	constraint fk_sender
	foreign key(sender)
	references users(pk_users),
	constraint fk_receiver
	foreign key(receiver)
	references users(pk_users)
);

create table photos (
	PK_PHOTOS int primary key generated always as identity,
	trip_id int not null,
	user_id int not null,
	constraint fk_tripid
	foreign key(trip_id)
	references trips(pk_trips) ON DELETE CASCADE,
	constraint fk_userid
	foreign key(user_id)
	references users(pk_users) ON DELETE CASCADE,
	location varchar
);

create table trip_participant (
	user_id int not null,
	trip_id int not null,
	constraint fk_tripid
	foreign key(trip_id)
	references trips(pk_trips) ON DELETE CASCADE,
	constraint fk_userid
	foreign key(user_id)
	references users(pk_users) ON DELETE CASCADE,
	status varchar
);
	
create table friends (
	user1_id int not null,
	user2_id int not null,
	constraint fk_user1
	foreign key(user1_id)
   references users(pk_users) ON DELETE CASCADE,
	constraint fk_user2
	foreign key(user2_id)
	references users(pk_users) ON DELETE CASCADE
);

create table ground_transportation (
	PK_GROUND_TRANSPORTATION int primary key generated always as identity,
   trip_id int not null,
	constraint fk_tripid
	foreign key(trip_id)
	references trips(pk_trips) ON DELETE CASCADE,
	airline varchar,
	fromID varchar,
	toID varchar,
	departure_time timestamp,
	arrival_time timestamp,
	has_air_con boolean,
	has_wifi boolean,
	price int,
	published_at timestamp,
	owner_id int,
	latitude float,
	longitude float,
   created_at TIMESTAMP NOT NULL,
   updated_at TIMESTAMP NOT NULL
);


create table ground_transportation_reservations (
   PK_GROUND_TRANSPORTATION_RESERVATION int primary key generated always as identity,
   ground_transportation int,
   constraint fk_ground_transportation
   foreign key(ground_transportation)
   references ground_transportation(PK_GROUND_TRANSPORTATION) ON DELETE CASCADE,
   reservation_date timestamp
);

create table ground_transportation_ticket (
   PK_GROUND_TRANSPORTATION_TICKET int primary key generated always as identity,
   ground_transportation_reservations int,
   constraint fk_ground_transportation_reservations
   foreign key(ground_transportation_reservations)
   references ground_transportation_reservations(PK_GROUND_TRANSPORTATION_RESERVATION) ON DELETE CASCADE,
   ticketID varchar,
   transportation_number varchar,
	name varchar,
	date timestamp,
    seat_number varchar,
	price int,
	date_purchase timestamp
);

create table flights (
   PK_FLIGHTS int primary key generated always as identity,
   trip_id int not null,
   constraint fk_tripid
   foreign key(trip_id)
   references trips(pk_trips) ON DELETE CASCADE,
   flight_number varchar,
   airline varchar,
   fromID varchar,
   toID varchar,
   departure_time timestamp,
   departure_date timestamp,
   arrival_time timestamp,
   has_air_con boolean,
   has_wifi boolean,
   price int,
   published_at	timestamp,
   owner_id int,
   latitude float,
   longitude float,
   created_at TIMESTAMP NOT NULL,
   updated_at TIMESTAMP NOT NULL
);

create table flights_reservations (
   PK_FLIGHTS_RESERVATIONS int primary key generated always as identity,
   flights_id int,
   constraint fk_flights_id
   foreign key(flights_id)
   references flights(PK_FLIGHTS) ON DELETE CASCADE ,
   reservation_date timestamp
);

create table flights_reservations_ticket (
   PK_RESERVATION_TICKET int primary key generated always as identity,
   flights_reservations_id int,
   constraint fk_flights_reservations_id
   foreign key(flights_reservations_id)
   references flights_reservations(PK_FLIGHTS_RESERVATIONS) ON DELETE CASCADE,
   ticketID varchar,
   flight_number varchar,
   name varchar,
   date timestamp,
   seat_number varchar,
   price int,
   date_purchase timestamp
);

create table stays (
  PK_STAYS int primary key generated always as identity,
  trip_id int not null,
  constraint fk_tripid
  foreign key(trip_id)
  references trips(pk_trips) ON DELETE CASCADE,
  room_id int,
  start_date timestamp,
  end_date timestamp,
  price	int,
  total	int,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

create table stays_reservations (
   PK_STAYS_RESERVATIONS int primary key generated always as identity,
   flights_id int,
   constraint fk_flights_id
   foreign key(flights_id)
   references flights(PK_FLIGHTS) ON DELETE CASCADE,
   reservation_date timestamp
);

create table rooms (
   PK_ROOMS int primary key generated always as identity,
   stays_reservations_id int,
   constraint fk_stays_reservations_id
   foreign key(stays_reservations_id)
   references stays_reservations(PK_STAYS_RESERVATIONS) ON DELETE CASCADE,
   home_type varchar,
   room_type varchar,
   total_occupancy int,
   total_bedrooms int,
   total_bathrooms int,
   summary varchar,
   address varchar,
   has_kitchen boolean,
   has_air_con boolean,
   has_wifi boolean,
   price int,
   published_at timestamp,
   owner_id int,
   created_at timestamp NOT NULL,
   updated_at timestamp NOT NULL,
  latitude float,
  longitude	float
);

create table made_payments (
   PK_MADE_PAYMENTS int primary key generated always as identity,
   creditcardID int,
   
   rooms_id int,
   constraint fk_rooms_id
   foreign key(rooms_id)
   references rooms(PK_ROOMS),
   
   flights_reservations_ticket int,
   constraint fk_flights_reservations_ticket
   foreign key(flights_reservations_ticket)
   references flights_reservations_ticket(PK_RESERVATION_TICKET) ON DELETE CASCADE,
   
   ground_transportation_ticket int,
   constraint fk_ground_transportation_ticket
   foreign key(ground_transportation_ticket)
   references ground_transportation_ticket(PK_GROUND_TRANSPORTATION_TICKET) ON DELETE CASCADE
 )
