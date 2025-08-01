# Amazon Bedrock Agents - How It Works Flow Diagram

## 1. High-Level Architecture Flow

```mermaid
graph TB
    User[👤 Customer] --> FURL[🔗 Lambda Function URL]
    FURL --> QueryLambda[⚡ Query Lambda Function]
    QueryLambda --> BedrockAgent[🤖 Amazon Bedrock Agent]
    
    subgraph "Agent Components"
        BedrockAgent --> FM[🧠 Foundation Model<br/>Claude/Titan/Llama]
        BedrockAgent --> KB[📚 Knowledge Base<br/>Company Data]
        BedrockAgent --> AG[🔧 Action Groups<br/>Lambda Functions]
    end
    
    subgraph "External Systems"
        AG --> Hotel[🏨 Hotel Booking API]
        AG --> Spa[💆 Spa Booking API]
        AG --> Golf[⛳ Golf Booking API]
    end
    
    BedrockAgent --> Response[📤 Orchestrated Response]
    Response --> User
    
    style BedrockAgent fill:#ff9999
    style FM fill:#99ccff
    style KB fill:#99ff99
    style AG fill:#ffcc99
```

## 2. Detailed Agent Processing Flow

```mermaid
sequenceDiagram
    participant C as Customer
    participant QL as Query Lambda
    participant BA as Bedrock Agent
    participant FM as Foundation Model
    participant KB as Knowledge Base
    participant AG as Action Group
    participant ES as External Systems
    
    C->>QL: Send prompt via Function URL
    QL->>BA: Invoke agent with request
    
    Note over BA: Agent Orchestration Begins
    
    BA->>FM: Process user input with instructions
    FM->>BA: Generate execution plan
    
    alt Knowledge Base Query Needed
        BA->>KB: Retrieve relevant information
        KB->>BA: Return company data/policies
    end
    
    alt Action Required
        BA->>AG: Invoke action group (Lambda)
        AG->>ES: Call external APIs/services
        ES->>AG: Return results
        AG->>BA: Format and return response
    end
    
    BA->>FM: Process results and generate response
    FM->>BA: Final response with context
    BA->>QL: Return orchestrated response
    QL->>C: Stream response back to customer
```

## 3. Agent Internal Processing (ReAct Framework)

```mermaid
graph TD
    Input[📝 User Input] --> Thought[🤔 THOUGHT<br/>Analyze request & plan]
    Thought --> Action[⚡ ACTION<br/>Execute tool/query KB]
    Action --> Observe[👁️ OBSERVE<br/>Evaluate results]
    Observe --> Decision{Goal<br/>Achieved?}
    
    Decision -->|No| Thought
    Decision -->|Yes| Response[📤 Final Response]
    
    subgraph "Available Actions"
        Action --> KB_Query[📚 Query Knowledge Base]
        Action --> API_Call[🔧 Call Action Group]
        Action --> Code_Exec[💻 Execute Code]
    end
    
    style Thought fill:#ffeb3b
    style Action fill:#4caf50
    style Observe fill:#2196f3
    style Decision fill:#ff9800
```

## 4. Complete Example: Hotel Booking Workflow

```mermaid
graph TB
    Start[🗣️ "Book a hotel room on 2024-02-25"] --> Agent[🤖 Bedrock Agent]
    
    Agent --> Step1[🤔 THOUGHT: Need to check availability]
    Step1 --> Action1[⚡ ACTION: GET /rooms API]
    Action1 --> Lambda1[⚡ Action Group Lambda]
    Lambda1 --> HotelAPI1[🏨 Hotel System: Get Available Rooms]
    HotelAPI1 --> Observe1[👁️ OBSERVE: List of available rooms]
    
    Observe1 --> Step2[🤔 THOUGHT: Present options to user]
    Step2 --> UserChoice[👤 User selects: "Deluxe room for $160"]
    
    UserChoice --> Step3[🤔 THOUGHT: Need to book selected room]
    Step3 --> Action2[⚡ ACTION: POST /rooms API]
    Action2 --> Lambda2[⚡ Action Group Lambda]
    Lambda2 --> HotelAPI2[🏨 Hotel System: Book Room 109]
    HotelAPI2 --> Observe2[👁️ OBSERVE: Booking confirmed]
    
    Observe2 --> Final[📤 "Room 109 booked for 2024-02-25, $160"]
    
    style Agent fill:#ff9999
    style Step1 fill:#ffeb3b
    style Step2 fill:#ffeb3b
    style Step3 fill:#ffeb3b
    style Action1 fill:#4caf50
    style Action2 fill:#4caf50
    style Observe1 fill:#2196f3
    style Observe2 fill:#2196f3
```

## 5. Multi-Agent Patterns

### A. Supervisor Pattern
```mermaid
graph TB
    User[👤 User Request] --> Supervisor[🎯 Supervisor Agent]
    
    Supervisor --> Hotel[🏨 Hotel Agent]
    Supervisor --> Spa[💆 Spa Agent]
    Supervisor --> Golf[⛳ Golf Agent]
    
    Hotel --> HotelComplete[✅ Hotel Task Complete]
    Spa --> SpaComplete[✅ Spa Task Complete]
    Golf --> GolfComplete[✅ Golf Task Complete]
    
    HotelComplete --> Supervisor
    SpaComplete --> Supervisor
    GolfComplete --> Supervisor
    
    Supervisor --> FinalResponse[📤 Coordinated Response]
    FinalResponse --> User
    
    style Supervisor fill:#ff6b6b
```

### B. Event-Driven Broker Pattern
```mermaid
graph TB
    Event[📨 Incoming Event] --> EventBridge[⚡ Amazon EventBridge]
    EventBridge --> BrokerLambda[🔀 Agent Broker Lambda]
    
    BrokerLambda --> AppConfig[⚙️ AWS AppConfig<br/>Agent Tool Context]
    AppConfig --> BrokerLambda
    
    BrokerLambda --> Converse[🤖 Bedrock Converse API<br/>Tool Selection]
    Converse --> BrokerLambda
    
    BrokerLambda --> SQS1[📬 SQS Queue 1]
    BrokerLambda --> SQS2[📬 SQS Queue 2]
    BrokerLambda --> SQS3[📬 SQS Queue 3]
    
    SQS1 --> SageMaker[🧠 SageMaker Agent]
    SQS2 --> BedrockAgent[🤖 Bedrock Agent]
    SQS3 --> External[🌐 External Agent]
    
    style BrokerLambda fill:#4ecdc4
    style Converse fill:#45b7d1
```

## 6. Technical Stack Components

```mermaid
graph LR
    subgraph "Frontend/Interface"
        User[👤 User]
        API[🔗 Function URL]
    end
    
    subgraph "Processing Layer"
        Lambda[⚡ AWS Lambda]
        Agent[🤖 Bedrock Agent]
    end
    
    subgraph "AI/ML Services"
        Models[🧠 Foundation Models<br/>Claude, Titan, Llama]
        Bedrock[🏗️ Amazon Bedrock]
    end
    
    subgraph "Data Layer"
        KB[📚 Knowledge Base]
        OpenSearch[🔍 OpenSearch Serverless]
        S3[📦 S3 Bucket<br/>OpenAPI Schema]
    end
    
    subgraph "Integration Layer"
        ActionGroups[🔧 Action Groups]
        ExternalAPIs[🌐 External APIs]
    end
    
    subgraph "Infrastructure"
        IAM[🔐 IAM Roles]
        CloudWatch[📊 CloudWatch Logs]
        EventBridge[⚡ EventBridge]
    end
    
    User --> API
    API --> Lambda
    Lambda --> Agent
    Agent --> Models
    Agent --> KB
    Agent --> ActionGroups
    KB --> OpenSearch
    ActionGroups --> ExternalAPIs
    Agent --> S3
```

## 7. Cost and Performance Considerations

```mermaid
graph TD
    subgraph "Cost Factors"
        OpenSearch[🔍 OpenSearch Serverless<br/>~$700/month baseline]
        Bedrock[🤖 Bedrock Models<br/>Pay per token]
        Lambda[⚡ Lambda<br/>Pay per invocation]
        Storage[📦 S3 Storage<br/>Minimal cost]
    end
    
    subgraph "Performance Optimizations"
        Streaming[📡 Response Streaming]
        Caching[💾 Session Caching]
        Parallel[⚡ Parallel Processing]
        CustomOrch[🎯 Custom Orchestration]
    end
    
    subgraph "Monitoring"
        Traces[🔍 X-Ray Tracing]
        Metrics[📊 CloudWatch Metrics]
        Logs[📝 Detailed Logging]
    end
```

## Key Features Highlighted:

1. **Orchestration**: Agent coordinates multiple services and APIs
2. **Context Awareness**: Maintains conversation history and session state
3. **Dynamic Routing**: Intelligently selects appropriate tools/actions
4. **Scalability**: Serverless architecture scales automatically
5. **Flexibility**: Event-driven patterns support complex workflows
6. **Monitoring**: Comprehensive observability and tracing
7. **Security**: IAM-based access control and guardrails