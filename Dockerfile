FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy only backend source
COPY springboot-backend/ .

# Build the JAR inside Docker
RUN ./mvnw clean package -DskipTests

# Copy the built jar
RUN cp target/*.jar app.jar

EXPOSE 10000

CMD ["java", "-jar", "app.jar"]
