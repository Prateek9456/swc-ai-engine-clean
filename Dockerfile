FROM eclipse-temurin:17-jdk

WORKDIR /app

COPY springboot-backend/target/*.jar app.jar

EXPOSE 10000

CMD ["java", "-jar", "app.jar"]
