# Challenges

Operations on multiple challenges.

## Synopsis

    evalai challenges

## Description

This command is used to fetch all the challenges that are currently active on EvalAI. It returns the following details of a challenge.

- Title
- ID
- Description
- End-Date

## Flags

### - -participant / -p

Returns the challenges that you've participated in.

### - -host / -h

Returns the challenges that you've hosted.

### Example Usage

    evalai challenges --participant # Fetch the challenges you've participated in.

## Arguments

### ongoing

List the challenges that are currently active.

### past

List all the past challenges.

### future

List all the upcoming challenges.

### Example Usage

    evalai challenges ongoing # Fetch current ongoing challenges
