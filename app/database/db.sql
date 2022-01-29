CREATE TABLE "User" (
	"id" serial NOT NULL,
	"name" varchar(255) NOT NULL UNIQUE,
	"password" varchar(255) NOT NULL,
	CONSTRAINT "User_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "File" (
	"id" serial NOT NULL,
	"name" varchar(255) NOT NULL,
	"access_id" integer NOT NULL DEFAULT '1',
	"user_id" integer NOT NULL,
	"number_of_downloads" integer NOT NULL DEFAULT '0',
	CONSTRAINT "File_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "Access" (
	"id" serial NOT NULL,
	"name" varchar(255) NOT NULL UNIQUE,
	"description" varchar(255) NOT NULL,
	CONSTRAINT "Access_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "public"."File" ADD CONSTRAINT "File_fk0" FOREIGN KEY ("access_id") REFERENCES "Access"("id");
ALTER TABLE "public"."File" ADD CONSTRAINT "File_fk1" FOREIGN KEY ("user_id") REFERENCES "User"("id");



INSERT INTO public."Access"(
	id, name, description)
	VALUES (1, 'all', 'Доступен всем'),
	VALUES (2, 'link', 'Доступен только по ссылке'),
	VALUES (3, 'private', 'Доступен только мне');
