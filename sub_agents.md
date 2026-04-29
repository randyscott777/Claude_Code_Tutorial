# Sub Agents

## Sub agents are specialized agents that can be invoked by the main agent to perform specific tasks. They can be used to break down complex problems into smaller, more manageable pieces, and to leverage the strengths of different types of agents.

### Example Use Cases for Sub Agents
1. **Data Retrieval**: A sub agent can be responsible for fetching data from a specific source, such as a database or an API, and returning it to the main agent for processing.  
2. **Data Processing**: A sub agent can be designed to perform specific data processing tasks, such as cleaning, transforming, or analyzing data, and then return the results to the main agent.
3. **Task Automation**: A sub agent can be used to automate specific tasks, such as sending emails, scheduling appointments, or managing files, allowing the main agent to focus on higher-level decision-making.
4. **Specialized Knowledge**: A sub agent can be created to have expertise in a specific domain, such as finance, healthcare, or legal, and can provide insights or recommendations based on that expertise when invoked by the main agent.
5. **Multi-Agent Collaboration**: Multiple sub agents can be designed to work together on a complex problem, with each sub agent handling a specific aspect of the problem and communicating with each other to achieve a common goal.
### Benefits of Using Sub Agents
- **Modularity**: Sub agents allow for a modular approach to problem-solving, where different components can be developed and maintained independently.
- **Scalability**: Sub agents can be added or removed as needed, allowing the system to scale up or down based on the complexity of the tasks at hand.
- **Specialization**: Sub agents can be designed to have specific expertise, allowing for more efficient and effective problem-solving.
- **Flexibility**: Sub agents can be invoked as needed, allowing the main agent to adapt to changing circumstances and requirements.
- **Improved Performance**: By delegating specific tasks to sub agents, the main agent can focus on higher-level decision-making, potentially improving overall performance and efficiency.
### Best Practices for Implementing Sub Agents
1. **Define Clear Interfaces**: Ensure that the main agent and sub agents have well-defined interfaces for communication, including input and output formats, to facilitate seamless interaction.
2. **Encapsulate Functionality**: Design sub agents to encapsulate specific functionality, allowing for easier maintenance and updates without affecting the main agent or other sub agents.
3. **Use Appropriate Communication Protocols**: Choose communication protocols that are suitable for the tasks being performed by the sub agents, such as REST APIs, message queues, or direct function calls.
4. **Monitor and Manage Sub Agents**: Implement monitoring and management tools to track the performance and health of sub agents, allowing for timely intervention if issues arise.
5. **Ensure Security and Privacy**: When designing sub agents, consider security and privacy implications, especially if they handle sensitive data or perform critical tasks, and implement appropriate safeguards to protect against potential threats.
### Conclusion
Sub agents can be a powerful tool for enhancing the capabilities of a main agent by allowing it to delegate specific tasks to specialized agents. By following best practices for implementation, organizations can leverage sub agents to improve modularity, scalability, specialization, flexibility, and performance in their systems.

# Sub-Agents Usage
There are three ways to invoke it:

  1. Ask in natural language (Claude auto-routes based on the agent's description):
  review the django_todo app for security vulnerabilities

  2. Explicitly name the agent:
  use the security-reviewer agent to audit todo_flask/app.py

  3. Via the /agents slash command to list/manage agents, then invoke.

  Note: there's also a built-in /security-review skill (listed in your available skills) that reviews
   pending changes on the current branch. That's a separate, ready-made path if you want a security
  pass on what you're working on right now rather than on a specific file.


  