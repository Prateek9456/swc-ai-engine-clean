FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy everything
COPY . .

# Build the jar
RUN ./mvnw clean package -DskipTests

# Expose Render port
EXPOSE 10000

# Run app
CMD ["java", "-jar", "target/*.jar"]
