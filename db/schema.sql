create table patients (
  id serial primary key,
  first_name varchar(50),
  last_name varchar(50),
  member_id varchar(20) unique not null
);

create table claims (
  id serial primary key,
  claim_id varchar(20) unique not null,
  claim_amount decimal(10,2),
  patient_id int references patients(id)
);

create table transactions (
  id serial primary key,
  edi_filename varchar(255),
  sender_id varchar(20),
  receiver_id varchar(20),
  transaction_date date
)