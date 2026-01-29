FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy only Spring Boot backend
COPY springboot-backend/ .

# Fix permission
RUN chmod +x mvnw

# Build jar
RUN ./mvnw clean package -DskipTests

EXPOSE 10000

CMD ["java", "-jar", "target/*.jar"]
