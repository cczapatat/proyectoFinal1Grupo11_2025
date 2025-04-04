package com.smartstock.myapplication


import android.view.View
import android.view.ViewGroup
import androidx.test.espresso.Espresso.onData
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.Espresso.pressBack
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.*
import androidx.test.espresso.matcher.RootMatchers
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import org.hamcrest.Description
import org.hamcrest.Matcher
import org.hamcrest.Matchers.allOf
import org.hamcrest.Matchers.anything
import org.hamcrest.Matchers.`is`
import org.hamcrest.TypeSafeMatcher
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@LargeTest
@RunWith(AndroidJUnit4::class)
class RegisterClientOK {

    @Rule
    @JvmField
    var mActivityScenarioRule = ActivityScenarioRule(SplashActivity::class.java)

    @Test
    fun registerClientOK() {
        val textInputEditText = onView(
            allOf(
                withId(R.id.email),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField5),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText.perform(replaceText("camilo@sta.com"), closeSoftKeyboard())

        val textInputEditText2 = onView(
            allOf(
                withId(R.id.password),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField6),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText2.perform(replaceText("1234567"), closeSoftKeyboard())

        pressBack()

        val materialButton = onView(
            allOf(
                withId(R.id.buttonLogin),
                childAtPosition(
                    allOf(
                        withId(R.id.section_11),
                        childAtPosition(
                            withId(R.id.logintest),
                            5
                        )
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialButton.perform(click())

        val bottomNavigationItemView = onView(
            allOf(
                withId(R.id.nav_menu), withContentDescription("Menu"),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.bottom_navigation),
                        0
                    ),
                    1
                ),
                isDisplayed()
            )
        )
        bottomNavigationItemView.perform(click())

        val materialTextView = onView(
            allOf(
                withId(android.R.id.title), withText("Crear Cliente"),
                childAtPosition(
                    childAtPosition(
                        withId(android.R.id.content),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialTextView.perform(click())

        val textInputEditText3 = onView(
            allOf(
                withId(R.id.name),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField4_1),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText3.perform(replaceText("prueba"), closeSoftKeyboard())

        val textInputEditText4 = onView(
            allOf(
                withId(R.id.address),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField4_2),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText4.perform(replaceText("AVENIDA 100"), closeSoftKeyboard())

        val textInputEditText5 = onView(
            allOf(
                withId(R.id.phone),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField4_3),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText5.perform(replaceText("+573000000341"), closeSoftKeyboard())


        textInputEditText5.perform(closeSoftKeyboard())

        pressBack()

        val materialAutoCompleteTextView = onView(
            allOf(
                withId(R.id.autoCompleteTextViewCreate1),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField4_5),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialAutoCompleteTextView.perform(click())

        onView(withText("Supermercado")) // Replace with actual dropdown item text
            .inRoot(RootMatchers.isPlatformPopup()) // Ensures it's in a popup
            .perform(click())
        onView(withText("Sur")) // Replace with actual dropdown item text
            .inRoot(RootMatchers.isPlatformPopup()) // Ensures it's in a popup
            .perform(click())
        /*val materialTextView2 = onData(anything())
            .inAdapterView(
                childAtPosition(
                    withClassName(`is`("android.widget.PopupWindow$PopupBackgroundView")),
                    0
                )
            )
            .atPosition(0)
        materialTextView2.perform(click())

        val materialAutoCompleteTextView2 = onView(
            allOf(
                withId(R.id.autoCompleteTextViewCreate2),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField4_6),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialAutoCompleteTextView2.perform(click())

        val materialTextView3 = onData(anything())
            .inAdapterView(
                childAtPosition(
                    withClassName(`is`("android.widget.PopupWindow$PopupBackgroundView")),
                    0
                )
            )
            .atPosition(4)
        materialTextView3.perform(click())*/

        val materialButton2 = onView(
            allOf(
                withId(R.id.buttonAcceptCreate), withText("Crear"),
                childAtPosition(
                    allOf(
                        withId(R.id.section_11),
                        childAtPosition(
                            withId(R.id.registerclienttest),
                            7
                        )
                    ),
                    1
                ),
                isDisplayed()
            )
        )
        materialButton2.perform(click())

        val textView = onView(
            allOf(
                withId(R.id.crear_nueva), withText("Lista de Clientes"),
                withParent(
                    allOf(
                        withId(R.id.section_4),
                        withParent(withId(R.id.listremindertest))
                    )
                ),
                isDisplayed()
            )
        )
        textView.check(matches(withText("Lista de Clientes")))
    }

    private fun childAtPosition(
        parentMatcher: Matcher<View>, position: Int
    ): Matcher<View> {

        return object : TypeSafeMatcher<View>() {
            override fun describeTo(description: Description) {
                description.appendText("Child at position $position in parent ")
                parentMatcher.describeTo(description)
            }

            public override fun matchesSafely(view: View): Boolean {
                val parent = view.parent
                return parent is ViewGroup && parentMatcher.matches(parent)
                        && view == parent.getChildAt(position)
            }
        }
    }
}
