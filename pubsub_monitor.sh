#!/usr/bin/env bash
  
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# "---------------------------------------------------------"
# "-                                                       -"
# "-  Setup environment variable                           -"
# "-  Run the PubSub subscription counter script           -"
# "-                                                       -"
# "---------------------------------------------------------"

set -o errexit
set -o nounset
set -o pipefail

WORKDIR=$HOME/scripts
export GOOGLE_APPLICATION_CREDENTIALS=$WORKDIR/log-pubsub-sa.json
cd $WORKDIR
echo `date` ":start..."  >> subscription_counter.log
# Add logic to check long running job and wait for it to finish
python subscription_counter.py 2>&1 >> subscription_counter.log
echo `date` ":finished"  >> subscription_counter.log
echo >> subscription_counter.log
