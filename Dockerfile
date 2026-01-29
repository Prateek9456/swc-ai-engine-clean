FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy project files
COPY . .

# 🔥 FIX PERMISSION ISSUE
RUN chmod +x mvnw

# Build the jar
RUN ./mvnw clean package -DskipTests

# Render uses dynamic port
EXPOSE 10000

# Run Spring Boot
CMD ["java", "-jar", "target/*.jar"]
