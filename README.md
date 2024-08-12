## Lead

A small app used to load students, their degrees and subjects and persist them in a database, powered by FastAPI and React. 

## Functional aspects

The app allows to load a student with its information, alongside many careers and the subjects associated with each one of them, in a dynamic form. It has validations to ensure the user cannot enter values that'll end up in a server error. The app assumes a scenario where everything is loaded at once, but it also has the foundations to build new scenarios in the future (for instance, loading degrees and subjects separately, and modifying the lead form to link to them instead of creating them simultaneously). The subjects and degrees will be added to the db independently, but not duplicated if a user tries to create a new degree with the same name or a new subject with the same name and degree-belonging. New lead, however, will be assigned to the other elements, whether they are created just before or are found as already existing in the database. 

After posting a lead, the id will return to the user in the UI and, afterwards, the FastAPI OpenAPI interface can be used to check the result. And Adminer instance, which allows to check the database status on your browser, is also deployed. 

## Technical aspects

The app is built with FastAPI in the backend and a Postgres database. In the ORM layer it uses SQLModel, a layer of compatibility over  Pydantic and SQLAlchemy recently built by the creator of FastAPI. Although the experiment was very interesting, since it's in a relatively early stage of development, sticking to the traditional use of Pydantic + SQLAlchemy may be advisable for larger projects aimed for production. All the environment is also configured to use MyPy for static type checking, trying to emulate best practices in that field. In Database terms, a strategy of generating different tables for subjects, degrees and leads was chosen, as well as intermediate tables to connect lead with subjects and degrees, aiming for an organization that could potentially scale, even if this is just a small exercise. 

The Front End was built with Vite, the Rust-based SWC compiler, and React. It also uses Typescript to leverage the Zod data validation library, which integrates well with React Hook Form. These type validations work really well and, when used thoughtfully, improve the developer's experience and diminish the chances of major errors. 

The database, the Back End and the Front End are organized to launch as Docker containers, with Docker-compose. It's important to notice that the repos configuration is aimed at a develop environment, serving to "early-test" the functioning of the app in a container environment, with hot reload. In production, the setup should be a bit different, mostly in the Front End, which should be built as static files and accessed through a web server (like Nginx) pointing to its index.html file. Also, a proper security configuration and CORS policy should be set before deploying.
## How to run

To run the project you need a PC with Docker installed. If Makefiles work in your environment (as they do by default on WSL, MacOS and Linux), you can simply use

``` shell
make
```

If not, you can use:

```bash
docker-compose up
```

After creating some leads from the UI, you can navigate to http://localhost:5000/docs
to check in the Back End only methods. There is a get-by-id method where you can check your recently created lead, and a fetch-all method with pagination you can use to consult multiple leads. 

You can also log to  http://localhost:8080 to enter the adminer interface, which will allow you to check the status of the docker PostgreSQL database in your browser, and see how. You can log with the following credentials:


|          |            |
| -------- | ---------- |
| System   | PostgreSQL |
| Server   | database   |
| Username | postgres   |
| Password | example    |
| Database | postgres   |
