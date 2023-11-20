## Что это
Различные конфиги. Для выкладывания на гитхаб, чтобы был доступ из любого места

Содержит:
  * конфигурация checkstyle для проектов java
  * конфигурация intellij idea
  * конфигурация для oh-my-zsh
  * открытые ключи GPG

## checkstyle config
Для использования с внутренним maven-репозиторием с доступом по ssh в файле c:/Users/<user>/.gradle/gradle.properties или $GRADLE_USER_HOME/gradle.properties прописываем данные
```properties
systemProp.mvn.publish.url=sftp://host:port/path/to/directory/
systemProp.mvn.publish.username=username
systemProp.mvn.publish.password=password
```

Для использования конфигурации checkstyle сначала публикуем этот проект на каком-нибудь репозитории maven:
```
./gradlew publish
```
и используем в других проектах на основе gradle:
```groovy
plugins {
    id("java")
    id("checkstyle")
}

repositories {
    mavenCentral()
    maven {
        url = uri(System.getProperty("mvn.publish.url"))
        credentials {
            username = System.getProperty("mvn.publish.username")
            password = System.getProperty("mvn.publish.password")
        }
    }
}

configurations {
    checkstyleConfig
}

// чтобы всегда качалась самая свежая версия
configurations.configureEach { resolutionStrategy.cacheChangingModulesFor(4, "seconds") }

dependencies {
    // чтобы всегда качалась самая свежая версия
    checkstyleConfig("by.gto.library:checkstyle-config:+@zip").changing = true
}

checkstyle {
    toolVersion = "8.27"
    config = resources.text.fromArchiveEntry(
        configurations.checkstyleConfig, "checkstyle.xml")
}
```
