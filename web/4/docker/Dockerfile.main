# first stage: building the lab
FROM maven AS build

WORKDIR /app

COPY pom.xml . 
COPY src ./src
RUN mvn package

# second stage: running the lab
FROM ubuntu/jre:21-24.04_stable AS runtime

WORKDIR /app

COPY --from=build /app/target/lab-4-1.0.jar .
COPY dist ./dist

ENTRYPOINT ["java", "-jar", "lab-4-1.0.jar"]
CMD []