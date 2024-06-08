# AEMO WEM Inventory - supporting infrastructure

A Terraform project to deploy supporting components to an AWS account

It does not install but relies on

-   a deployment role with permission to deploy the stuff
-   a permission boundary that limits the scope of the roles we can create in this project

## C4 - System Context

This system (AEMO WEM inventory) interrogates another system (AEMO WEM Data Server - managed by AEMO) and generates a visualisation based on the data that is gathered.

```mermaid
C4Context
    title An approximate system context


    Boundary(mbRD, "This Repo") {
        System(aemowemInventory,"Inventory System","A system to catalogue and display visualisations on available files")
        Rel(me, aemowemInventory,"View Data","I like pretty dashboards")
    }
    Person(me, "Data Consumer", "I like Data")
    Boundary(mbAEMO, "Australian Energy Market Operator") {
        System_Ext(aemoServer, "AEMO WEM
        Data Server", "where the data is accessible")
        System_Ext(dude1, "Data Producers")
        Rel(dude1,aemoServer,"Put Files","regularly")
    }

    Rel(aemowemInventory,aemoServer,"Review File Entries","Navigate website pages and collection file statistics")
    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

### C4 - Container Diagram

The system in this repository:

-   periodically crawls the AEMO data server, following directory links, gathering statistics about files and directories, to form an _inventory_
-   writes _inventory_ results to S3
-   produces a duckdb database populated with the _inventory_ data from S3
-   builds a static website with [Evidence.dev](https://evidence.dev) and deploys it with CloudFront CDN backed by S3 Origin

```mermaid
C4Container
    title AEMO WEM - Inventory System - Container Diagram
    System_Boundary(aemo,"AEMO") {
        System_Ext(aemoData,"AEMO Data Site")
    }

    Container_Boundary(isc,"Inventory System") {
        Container_Ext(cwSchedule,"CloudWatch Scheduler")
        Container(lambda,"Lambda","Inventory Runner")
        Container(sfn,"Step Function")
        Container(s3Inventory,"S3","Inventory Location")
        Container(codebuild,"CodeBuild","DuckDb Runner")
        Container(cloudfront,"CloudFront","Evidence Distribution")
        Container(s3Evidence,"S3","Evidence Site Location")
        Container(s3Duckdb,"S3","Duckdb Location")
        Container(iamRole,"IAM", "Deploy Role")
    }
    System_Boundary(other,"Everything Else") {
        Container_Ext(actionInfra,"Action: Infra")
        Container_Ext(actionEvidence, "Action: Evidence")

        System_Ext(githubActions,"Github","Repository")
    }
    Rel(cwSchedule,sfn,"Trigger","Every 6 hours")
    Rel(githubActions,actionInfra,"Trigger","Terraform Deploy")
    Rel(githubActions,actionEvidence,"Trigger","Evidence Deploy")
    Rel(actionInfra,iamRole,"Deploy")
    Rel(actionEvidence,s3Evidence,"Publish")
    Rel(actionEvidence,s3Duckdb,"Copy duckdb")
    Rel(actionEvidence,cloudfront,"Invalidate")
    Rel(lambda,aemoData,"Interrogates")
    Rel(sfn,lambda,"Starts")
    Rel(lambda,codebuild,"Step Function Calls Next")
    Rel(codebuild,s3Inventory,"reads")
    Rel(codebuild,s3Duckdb,"writes")
    Rel(lambda,s3Inventory,"writes")
    Rel(codebuild,actionEvidence,"Dispatch","Calls Action to deploy Evidence with updated Duckdb")
    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")

```
