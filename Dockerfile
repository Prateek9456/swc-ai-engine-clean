FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy everything from repo
COPY . .

# Make mvnw executable if it exists
RUN chmod +x mvnw || true

# Build only if pom.xml exists
RUN if [ -f pom.xml ]; then \
      ./mvnw clean package -DskipTests; \
    else \
      cd */ && ./mvnw clean package -DskipTests; \
    fi

EXPOSE 10000

CMD ["sh", "-c", "java -jar $(find . -name '*.jar' | head -n 1)"]
