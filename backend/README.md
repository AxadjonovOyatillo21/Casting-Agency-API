# Casting Agency 🔥
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.
This is a Restful API written in Flask micro-framework.



## Introuction

The Casting Agency API based on RBAC(role based access control).

There are 3 roles:
  - Assistant
  - Director
  - Executive Producer

And this API had public endpoints too.

* All of this roles has their permissions
    * Assistant:
        - view:genres
        - view:actors
        - view:movies
        - view:genres
    * Director:
        - All permissions of assistant
        - add:actors
        - delete:actors
        - update:actors
        - update:movies
        - update:genres
    * Executive Producer:
        - All permissions of director
        - add:genres
        - add:movies
        - delete:genres
        - delete:movies

To testing this project, I've prepared default accounts for Assistant, Director and Producer.
> Email/Password of default accounts
>* @caAssistant@gmail.comp
>* @caDirector@gmail.comp
>* @caProducer@gmail.comp
>* Password: casting_agency123



