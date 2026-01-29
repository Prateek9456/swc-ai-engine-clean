FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy backend source
COPY springboot-backend/ .

# Build the jar inside Docker
RUN ./mvnw clean package -DskipTests

# Rename jar
RUN cp target/*.jar app.jar

EXPOSE 10000

CMD ["java", "-jar", "app.jar"]
