--create database
CREATE DATABASE

--grant access and privileges
GRANT ALL PRIVILEGES ON DATABASE fastapitest TO davidking;

--create extension for uuid
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

--create table
CREATE TABLE posts(
post_id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
title VARCHAR(255) NOT NULL,
content VARCHAR(255) NOT NULL,
published BOOLEAN NOT NULL DEFAULT true,
created_at TIMESTAMP NOT NULL DEFAULT now()
);

--insert dummy posts as seed data
INSERT INTO
posts(title,content)
VALUES
('SPY up today','Netflix a big loser on an up day from the SPY'),
('QQQ plunges','Tech stocks plunge on higher interest rates'),
('IWM flat','Small cap stocks unchanged as dollar continues its rise');
