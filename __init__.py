# Copyright 2018 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.
#
# Visit https://docs.mycroft.ai/skill.creation for more detailed information
# on the structure of this skill and its containing folder, as well as
# instructions for designing your own skill based on this template.


# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
from os import listdir
from os.path import dirname, isfile, join

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft import intent_handler
from mycroft.skills.context import adds_context, removes_context


__author__ = 'Charles'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class ContextSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(ContextSkill, self).__init__(name="ContextSkill")

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    @intent_handler(IntentBuilder('TeaIntent').require("TeaKeyword"))
    @adds_context('MilkContext')
    def handle_tea_intent(self, message):
        self.milk = False
        self.speak('Of course, would you like Milk with that?', expect_response=True)

    @intent_handler(IntentBuilder('NoMilkIntent').require("NoKeyword").require('MilkContext').build())
    @adds_context('HoneyContext')
    @removes_context('MilkContext')
    def handle_yes_milk_intent(self, message):
        self.milk = True
        self.speak('all right, any Honey?', expect_response=True)

    @intent_handler(IntentBuilder('YesMilkIntent').require("YesKeyword").require('MilkContext').build())
    @adds_context('HoneyContext')
    @removes_context('MilkContext')
    def handle_no_milk_intent(self, message):
        self.speak('What about Honey?', expect_response=True)

    @intent_handler(IntentBuilder('NoHoneyIntent').require("NoKeyword").require('HoneyContext').build())
    @removes_context('HoneyContext')
    def handle_no_honey_intent(self, message):
        if self.milk: #i.e., line 55 is still false
            self.speak('Heres your Tea, straight up')
        else:
            self.speak('Heres your Tea with a dash of Milk')

    @intent_handler(IntentBuilder('YesHoneyIntent').require("YesKeyword").require('HoneyContext').build())
    @removes_context('HoneyContext')
    def handle_yes_honey_intent(self, message):
        if self.milk: # there was a mistake originally here in the Mycroft guide. 
            self.speak('Heres your Tea with Honey')
        else:
            self.speak('Heres your Tea with Milk and Honey')
            
    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return ContextSkill()